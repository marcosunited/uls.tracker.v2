from mrs.serializers import *
from mrs.utils.filter import FilteredModelViewSet


class ProjectViewSet(FilteredModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer


class ContactViewSet(FilteredModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactsSerializer


class ContractViewSet(FilteredModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractsSerializer


class ContractFrequencyViewSet(FilteredModelViewSet):
    queryset = ContractFrequency.objects.all()
    serializer_class = ContractFrequenciesSerializer


class JobViewSet(FilteredModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer


class RoundViewSet(FilteredModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundsSerializer


class AgentViewSet(FilteredModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentsSerializer


class TechnicianViewSet(FilteredModelViewSet):
    queryset = Technician.objects.all()
    serializer_class = TechniciansSerializer


class LiftViewSet(FilteredModelViewSet):
    queryset = Lift.objects.all()
    serializer_class = LiftsSerializer


class CorrectionViewSet(FilteredModelViewSet):
    queryset = Correction.objects.all()
    serializer_class = CorrectionsSerializer


class FaultViewSet(FilteredModelViewSet):
    queryset = Fault.objects.all()
    serializer_class = FaultsSerializer
