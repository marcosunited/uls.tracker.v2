from rest_framework import serializers

from mrs.utils.cache import CachedModelViewSet


class FilteredModelViewSet(CachedModelViewSet):

    def get_queryset(self):
        model_class = self.Meta.model
        return model_class.objects.all()


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
