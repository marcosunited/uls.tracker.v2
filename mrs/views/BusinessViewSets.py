from django.db import transaction
from django.http import JsonResponse
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from mrs.serializers import *
from mrs.services.maintenanceService import MaintenanceService
from mrs.utils.cache import CachedModelViewSet
from mrs.utils.filter import FilteredModelViewSet
from mrs.utils.model import LogicalDeleteModelViewSet
from mrs.utils.response import ResponseHttp


class JhaItemViewSet(FilteredModelViewSet, CachedModelViewSet):
    queryset = JhaItem.objects.all()
    serializer_class = JhaItemsSerializer


class MetadataTypeViewSet(FilteredModelViewSet, CachedModelViewSet):
    queryset = MetadataType.objects.all()
    serializer_class = MetadataTypesSerializer


class MetadataValuesViewSet(FilteredModelViewSet, CachedModelViewSet):
    queryset = MetadataValue.objects.all()
    serializer_class = MetadataValuesSerializer


class ProjectViewSet(FilteredModelViewSet, LogicalDeleteModelViewSet):
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


# /rounds/idRound/technicians/idTec/
class RoundTechnicianRelationView(APIView):
    def post(self, request, pk_round, pk_technician):
        try:
            round = Round.objects.get(id=pk_round)
            technician = Technician.objects.get(id=pk_technician)
            round.technicians.add(technician.id)
            round_serializer = RoundsSerializer(round)
            return JsonResponse({'result': round_serializer.data})
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
            return JsonResponse({'result': round_serializer.data})
        except Round.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The round does not exist').result, status=HTTP_404_NOT_FOUND)
        except Technician.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The technician does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileViewSet(FilteredModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfilesSerializer


class ProjectProfileOptionsView(APIView):
    def get(self, request, pk_project):
        try:
            profiles_all = Profile.objects.all();
            project = Project.objects.get(id=pk_project)
            profile_options = [profile for profile in profiles_all if profile not in project.profile_set.all()]
            profile_serializer = ProfilesSerializer(profile_options, many=True)
            return JsonResponse({'result': profile_serializer.data})
        except Project.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The project does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# /profiles/idProfile/projects/idProject/
class ProfileProjectRelationView(APIView):
    def post(self, request, pk_profile, pk_project):
        try:
            profile = Profile.objects.get(id=pk_profile)
            project = Project.objects.get(id=pk_project)
            profile.projects.add(project.id)
            profile_serializer = ProfilesSerializer(profile)
            return JsonResponse({'result': profile_serializer.data})
        except Profile.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The profile does not exist').result, status=HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The project does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk_profile, pk_project):
        try:
            profile = Profile.objects.get(id=pk_profile)
            project = Project.objects.get(id=pk_project)
            profile.projects.remove(project.id)
            profile_serializer = ProfilesSerializer(profile)
            return JsonResponse({'result': profile_serializer.data})
        except Profile.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The profile does not exist').result, status=HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The project does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# /jobs/idJob/lifts/idLift/
class JobLiftRelationView(APIView):
    def post(self, request, pk_job, pk_lift):
        try:
            job = Job.objects.get(id=pk_job)
            lift = Lift.objects.get(id=pk_lift)
            job.lift_set.add(lift)
            job_serializer = JobsSerializer(job)
            return JsonResponse({'result': job_serializer.data})
        except Job.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The job does not exist').result, status=HTTP_404_NOT_FOUND)
        except Lift.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The lift does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk_job, pk_lift):
        try:
            job = Job.objects.get(id=pk_job)
            lift = Lift.objects.get(id=pk_lift)
            job.lift_set.remove(lift.id)
            job_serializer = JobsSerializer(job)
            return JsonResponse({'result': job_serializer.data})
        except Job.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The job does not exist').result, status=HTTP_404_NOT_FOUND)
        except Lift.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The lift does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


class GroupViewSet(FilteredModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer


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
            return JsonResponse({'result': jobs})
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


class ServiceTargetViewSet(FilteredModelViewSet):
    queryset = ServiceTarget.objects.all()
    serializer_class = ServiceTargetSerializer


class NoteViewSet(FilteredModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NotesSerializer


class ProcedureViewSet(FilteredModelViewSet):
    queryset = Procedure.objects.all()
    serializer_class = ProceduresSerializer


class OperationViewSet(FilteredModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationsSerializer


class ActionViewSet(FilteredModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionsSerializer


# /procedures/idProcedure/tasks/idTask/
class ProcedureTaskRelationView(APIView):
    def post(self, request, pk_procedure, pk_task):
        try:
            procedure = Procedure.objects.get(id=pk_procedure)
            task = Task.objects.get(id=pk_task)
            procedure.tasks.add(task)
            procedure_serializer = ProceduresSerializer(procedure)
            return JsonResponse({'result': procedure_serializer.data, 'error': ''})
        except Procedure.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The procedure does not exist').result, status=HTTP_404_NOT_FOUND)
        except Task.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The task does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk_procedure, pk_task):
        try:
            procedure = Procedure.objects.get(id=pk_procedure)
            task = Task.objects.get(id=pk_task)
            procedure.tasks.remove(task)
            procedure_serializer = ProceduresSerializer(procedure)
            return JsonResponse({'result': procedure_serializer.data, 'error': ''})
        except Procedure.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The procedure does not exist').result, status=HTTP_404_NOT_FOUND)
        except Task.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The task does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


class TaskViewSet(FilteredModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TasksSerializer


class MaintenancePlanViewSet(FilteredModelViewSet):
    queryset = MaintenancePlan.objects.all()
    serializer_class = MaintenancePlansSerializer


class GenerateMaintenancePlanView(APIView):
    @transaction.atomic
    def post(self, request, pk_lift):
        try:
            maintenance_service = MaintenanceService()
            plan = maintenance_service.generate_plan(pk_lift)
            return JsonResponse({'result': plan})
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def delete(self, request, pk_lift):
        try:
            return JsonResponse({'result': pk_lift, 'error': ''})
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ScheduleEntryViewSet(FilteredModelViewSet):
    queryset = ScheduleEntry.objects.all()
    serializer_class = ScheduleEntriesSerializer
