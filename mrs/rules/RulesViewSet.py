from mrs.models import Rule
from mrs.serializers import RulesSerializer
from mrs.utils.filter import FilteredModelViewSet


class RulesViewSet(FilteredModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RulesSerializer
