from mrs.utils.cache import CachedModelViewSet


class FilteredModelViewSet(CachedModelViewSet):

    def get_queryset(self):
        model_class = self.Meta.model
        return model_class.objects.all()
