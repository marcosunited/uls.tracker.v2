from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets


class CachedModelViewSet(viewsets.ModelViewSet):

    # TODO: reactivate cache
    ## @method_decorator(cache_page(60*60*2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
