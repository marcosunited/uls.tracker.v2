from mrs.serializers import *
from mrs.utils.cache import CachedModelViewSet
from mrs.utils.filter import FilteredModelViewSet


class ProjectViewSet(CachedModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer


class ContactViewSet(CachedModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactsSerializer


class ContractViewSet(CachedModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractsSerializer


class ContractFrequencyViewSet(CachedModelViewSet):
    queryset = ContractFrequency.objects.all()
    serializer_class = ContractFrequenciesSerializer


class JobViewSet(FilteredModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer


class RoundViewSet(CachedModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundsSerializer


class AgentViewSet(CachedModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentsSerializer


class TechnicianViewSet(CachedModelViewSet):
    queryset = Technician.objects.all()
    serializer_class = TechniciansSerializer

