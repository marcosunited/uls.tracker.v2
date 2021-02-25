import re

from django.apps import apps
from django.core.exceptions import FieldError
from django.db.models import Lookup, CharField, TextField, Count, Q
from django.db.models.fields import Field
from django.http import JsonResponse

from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter, Route, DynamicRoute
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from mrs.models import MrsField, MrsOperator, Project

from mrs.utils.response import ResponseHttp as ObjectResponse, ResponseHttp


def tokenize_text(text,
                  findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                  normspace=re.compile(r'\s{2,}').sub):
    return [normspace('', (t[0] or t[1]).strip()) for t in findterms(text)]


class Search(Lookup):
    lookup_name = 'search'

    def as_mysql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        # MySql specific implementation of full text search
        # TODO: dynamically add FULLTEXT index for all text fields in mysql db
        return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params


CharField.register_lookup(Search)
TextField.register_lookup(Search)


class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


Field.register_lookup(NotEqual)


class MrsOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MrsOperator
        fields = ('id',
                  'name',
                  'code',
                  'django_lookup')


class MrsFieldSerializer(serializers.ModelSerializer):
    operators = MrsOperatorSerializer(read_only=True, many=True)

    class Meta:
        model = MrsField
        fields = ('id',
                  'name',
                  'operators',
                  'isList',
                  'list_source_model')


class ModelMetaView(APIView):
    fields = []

    def get(self, request, model):
        model = apps.get_model('mrs', model)
        for _field in model._meta.fields:
            try:
                field = MrsField.objects.filter(name=_field.__class__.__name__)
                if field.count() == 1:
                    field = field[0]
                    if field:
                        field_serializer = MrsFieldSerializer(field)
                        self.fields.append({'name': _field.name,
                                            'display': _field.verbose_name,
                                            'isRelation': _field.is_relation,
                                            'meta': field_serializer.data})
                else:
                    for _nested_field in _field.related_model._meta.fields:
                        nested_field = MrsField.objects.filter(name=_nested_field.__class__.__name__)
                        if nested_field.count() == 1:
                            nested_field = nested_field[0]
                            if nested_field:
                                field_serializer = MrsFieldSerializer(nested_field)
                                self.fields.append({'name': _field.name + '__' + _nested_field.name,
                                                    'display': _nested_field.verbose_name,
                                                    'isRelation': _nested_field.is_relation,
                                                    'meta': field_serializer.data})
            except AttributeError as e:
                pass

        response = ObjectResponse(self.fields)

        return Response(response.result, status=HTTP_200_OK)


class ModelAggregationView(APIView):
    def get(self, request, model, field):
        try:
            model = model[:-1]
            model = apps.get_model('mrs', model)
            aggregations_result = model.objects.values(field).annotate(dcount=Count(field))
            aggregations_list = list()
            for aggregation in aggregations_result:
                aggregation_item = {"key": aggregation[field], "count": aggregation['dcount']}
                aggregations_list.append(aggregation_item)

            return JsonResponse({"result": aggregations_list}, safe=False)
        except model.DoesNotExist:
            return JsonResponse(ResponseHttp(error='Model does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


def get_q(entry):
    complex_query = None
    logical_operator = None
    for w in entry:
        if type(w) is list:
            q_field = w[0]
            q_operator = DynamicFilter.operators.get(w[1])
            q_value = w[2]
            if q_operator == 'between':
                q_second_value = w[3]

            _q = Q((q_field + q_operator, q_value))

            if complex_query is None:
                complex_query = _q

            if logical_operator is not None:
                if logical_operator == 'and':
                    complex_query = complex_query & _q
                else:
                    complex_query = complex_query | _q
        else:
            logical_operator = w

    return complex_query


class DynamicFilter:
    operators = {}

    def filter(self, query_set, data):
        query_list = None
        search = None
        order_by = None
        complex_query_list = None

        if not DynamicFilter.operators.keys():
            operators_setting = MrsOperator.objects.all()
            for _operator in operators_setting:
                DynamicFilter.operators.update({_operator.code: _operator.django_lookup})

        if type(data) is list:
            try:
                complex_query_list = data
            except KeyError:
                return query_set
        else:
            try:
                query_list = data["query"]
            except KeyError:
                query_list = None

            try:
                order_by = data["orderBy"]
            except KeyError:
                order_by = None

            try:
                search = data["search"]
            except KeyError:
                search = None

        complex_query = None
        entry_count = 0
        if complex_query_list:
            for entry in complex_query_list:
                if (entry_count + 1) == len(complex_query_list):
                    break
                if type(entry) is list:
                    complex_query = get_q(entry)  ##esta sobre escribiendo con el ultimo item de la lista
                else:
                    if entry == "and":
                        complex_query = complex_query & get_q(complex_query_list[entry_count + 1])
                    else:
                        complex_query = complex_query | get_q(complex_query_list[entry_count + 1])

                entry_count += 1
            query_set = query_set.filter(complex_query)

        kwargs = {}
        if query_list:
            try:
                if entry.get('operator') and entry.get('value'):
                    op = DynamicFilter.operators.get(entry.get('operator'))
                    kwargs.update({entry.get('field') + op: entry.get('value')})
                    query_set = query_set.filter(**kwargs)
            except Exception:
                pass

        if search:
            if search.get('fields') and search.get('text'):
                fields = search.get('fields')
                text = search.get('text')
                terms = tokenize_text(text)
                for term in terms:
                    or_query = None
                    for field_name in fields:
                        entry = Q(**{"%s__icontains" % field_name: term})
                        if or_query is None:
                            or_query = entry
                        else:
                            or_query = or_query | entry

                        query_set = query_set.filter(or_query)

        if order_by:
            for o in order_by:
                query_set = query_set.order_by(o)

        try:
            return query_set.filter(is_deleted=False)
        except FieldError:
            return query_set


class FilteredModelViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        query_set = super().get_queryset()
        if self.request.method == 'POST':
            dynamic_filter = DynamicFilter()
            return dynamic_filter.filter(query_set, self.request.data)
        return query_set


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        try:
            fields = self.context['request'].query_params.get('fields')
            if fields:
                fields = fields.split(',')
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)
        except Exception as e:
            pass


class QueryRouter(DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/query{trailing_slash}$',
            mapping={
                'post': 'list'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]
