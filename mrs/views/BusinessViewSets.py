from django.http import JsonResponse
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from mrs.serializers import *
from mrs.utils.filter import FilteredModelViewSet
from mrs.utils.response import ResponseHttp


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


# /rounds/idRound/addTech/idTec/
class RoundTechnicianRelationView(APIView):
    def post(self, request, pk_round, pk_technician):
        try:
            round = Round.objects.get(id=pk_round)
            technician = Technician.objects.get(id=pk_technician)
            round.technicians.add(technician.id)
            round_serializer = RoundsSerializer(round)
            return JsonResponse({'result': round_serializer.data, 'error': ''})
        except Round.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The round does not exist').result, status=HTTP_404_NOT_FOUND)
        except Technician.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The technician does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk_round, pk_technician):
        try:
            round = Round.objects.get(id=pk_round)
            technician = Technician.objects.get(id=pk_technician)
            round.technicians.remove(technician.id)
            round_serializer = RoundsSerializer(round)
            return JsonResponse({'result': round_serializer.data, 'error': ''})
        except Round.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The round does not exist').result, status=HTTP_404_NOT_FOUND)
        except Technician.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The technician does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


class AgentViewSet(FilteredModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentsSerializer


class TechnicianViewSet(FilteredModelViewSet):
    queryset = Technician.objects.all()
    serializer_class = TechniciansSerializer


# /technicians/idTechnician/getJobs
class TechnicianJobsRelationView(APIView):
    def get(self, request, pk_technician):
        try:
            project_id = self.request.query_params.get('projectId')
            technician = Technician.objects.get(id=pk_technician)
            rounds = technician.round_set.filter(project__id=project_id)
            jobs = []
            for _round in rounds:
                _jobs = _round.job_set.all()
                for job in _jobs:
                    jobs.append(JobsSerializer(job).data)
            return JsonResponse({'result': jobs, 'error': ''})
        except Technician.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The technician does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# /technicians/idTechnician/getCallouts
class TechnicianCalloutsRelationView(APIView):
    def get(self, request, pk_technician):
        try:
            project_id = self.request.query_params.get('projectId')
            technician = Technician.objects.get(id=pk_technician)
            workorders = technician.workorder_set.filter(process_type_name='CALLOUT',
                                                         project_id=project_id)
            callouts = []
            for workorder in workorders:
                callouts.append(CalloutsSerializer(workorder.callout).data)
            return JsonResponse({'result': callouts, 'error': ''})
        except Technician.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The technician does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# /technicians/idTechnician/getMaintenances
class TechnicianMaintenancesRelationView(APIView):
    def get(self, request, pk_technician):
        try:
            project_id = self.request.query_params.get('projectId')
            technician = Technician.objects.get(id=pk_technician)
            workorders = technician.workorder_set.filter(process_type_name='MAINTENANCE',
                                                         project_id=project_id)
            maintenances = []
            for workorder in workorders:
                maintenances.append(MaintenancesSerializer(workorder.maintenance).data)
            return JsonResponse({'result': maintenances, 'error': ''})
        except Technician.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The technician does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# /technicians/idTechnician/getRepairs
class TechnicianMaintenancesRelationView(APIView):
    def get(self, request, pk_technician):
        try:
            project_id = self.request.query_params.get('projectId')
            technician = Technician.objects.get(id=pk_technician)
            workorders = technician.workorder_set.filter(process_type_name='REPAIR',
                                                         project_id=project_id)
            repairs = []
            for workorder in workorders:
                repairs.append(RepairsSerializer(workorder.repair).data)
            return JsonResponse({'result': repairs, 'error': ''})
        except Technician.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The technician does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


class LiftViewSet(FilteredModelViewSet):
    queryset = Lift.objects.all()
    serializer_class = LiftsSerializer


class CorrectionViewSet(FilteredModelViewSet):
    queryset = Correction.objects.all()
    serializer_class = CorrectionsSerializer


class FaultViewSet(FilteredModelViewSet):
    queryset = Fault.objects.all()
    serializer_class = FaultsSerializer


class NoteViewSet(FilteredModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NotesSerializer

