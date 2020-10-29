from rest_framework import serializers
from rest_framework.routers import DefaultRouter, Route, DynamicRoute

from mrs.models import Settings
from mrs.utils.cache import CachedModelViewSet

from django.db.models import Lookup
from django.db.models.fields import Field


class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


# register ne (not equal) lookup to filter
# use: results = Model.objects.exclude(a=True, x__ne=5)
Field.register_lookup(NotEqual)


class FilteredModelViewSet(CachedModelViewSet):
    operators = {}

    def get_queryset(self):
        if not FilteredModelViewSet.operators.keys():
            queries_setting = Settings.objects.filter(module='APIQUERIES')
            for operator in queries_setting:
                FilteredModelViewSet.operators.update({operator.code: operator.value})

        query_set = super().get_queryset()
        if self.request.method == 'POST':
            query_list = self.request.data["query"]
            for q in query_list:
                kwargs = {}
                op = "__exact"
                if q.get('operator'):
                    op = FilteredModelViewSet.operators.get(q.get('operator'))
                kwargs.update({q.get('field') + op: q.get('value')})
                query_set = query_set.filter(**kwargs)
            return query_set
        return query_set


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


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
