from django.apps import apps
from django.core.exceptions import FieldError
from django.db.models import Lookup, CharField, TextField
from django.db.models.fields import Field

from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter, Route, DynamicRoute
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from mrs.models import MrsField, MrsOperator

from mrs.utils.response import ResponseHttp as ObjectResponse


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


class FilteredModelViewSet(viewsets.ModelViewSet):
    operators = {}

    def get_queryset(self):
        if not FilteredModelViewSet.operators.keys():
            operators_setting = MrsOperator.objects.all()
            for operator in operators_setting:
                FilteredModelViewSet.operators.update({operator.code: operator.django_lookup})

        query_set = super().get_queryset()
        if self.request.method == 'POST':
            try:
                query_list = self.request.data["query"]
            except KeyError:
                return query_set
            try:
                order_by = self.request.data["orderBy"]
            except KeyError:
                order_by = None

            kwargs = {}
            for q in query_list:
                if q.get('operator') and q.get('value'):
                    op = FilteredModelViewSet.operators.get(q.get('operator'))
                    kwargs.update({q.get('field') + op: q.get('value')})
                    query_set = query_set.filter(**kwargs)
            if order_by:
                for o in order_by:
                    query_set = query_set.order_by(o)

        try:
            return query_set.filter(is_deleted=False)
        except FieldError:
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
