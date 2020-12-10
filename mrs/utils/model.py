from django.db.models import ManyToManyField
from rest_framework import viewsets
from rest_framework.response import Response


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                try:
                    data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
                except Exception as e:
                    data[f.name] = []
        else:
            data[f.name] = f.value_from_object(instance)
    return data


class LogicalDeleteModelViewSet(viewsets.ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


