"""
mrs URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path

from mrs.reports import ReportsViewSet
from mrs.rules.RulesViewSet import RulesViewSet
from mrs.rules.rules import RulesMetaView
from mrs.utils.storage import FileView
from mrs.utils.filter import QueryRouter, ModelMetaView
from mrs.views import BusinessViewSets

from mrs.views.BusinessViewSets import *
from mrsauth.views import UserFilteredView

router = QueryRouter()

router.register(r'meta_types', MetadataTypeViewSet)
router.register(r'meta_values', MetadataValuesViewSet)

router.register(r'projects', ProjectViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'contract_frequencies', ContractFrequencyViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'rounds', RoundViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'technicians', TechnicianViewSet)
router.register(r'lifts', LiftViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'procedures', ProcedureViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'operations', OperationViewSet)
router.register(r'actions', ActionViewSet)
router.register(r'maintenance_plans', MaintenancePlanViewSet)
router.register(r'schedule_entries', ScheduleEntryViewSet)
router.register(r'jha_items', JhaItemViewSet)
router.register(r'corrections', CorrectionViewSet)
router.register(r'faults', FaultViewSet)
router.register(r'service_targets', ServiceTargetViewSet)
router.register(r'rules', RulesViewSet)
router.register(r'users', UserFilteredView)


urlpatterns = [
    # Django admin urls
    path('admin/', admin.site.urls),

    # auth app urls
    url(r'^', include('mrsauth.urls')),

    url(r'^api/v1/meta/(?P<model>\D+)/', ModelMetaView.as_view()),
    url(r'^api/v1/rules/meta/(?P<model>\D+)/', RulesMetaView.as_view()),
    url(r'^api/v1/upload/$', FileView.as_view(), name='file-upload'),
    url(r'^api/v1/', include(router.urls)),

    # rounds - technicians
    url(r'^api/v1/rounds/(?P<pk_round>[0-9]+)/technicians/(?P<pk_technician>[0-9]+)$',
        BusinessViewSets.RoundTechnicianRelationView.as_view()),

    # profiles - projects
    url(r'^api/v1/profiles/(?P<pk_profile>[0-9]+)/projects/(?P<pk_project>[0-9]+)$',
        BusinessViewSets.ProfileProjectRelationView.as_view()),

    url(r'^api/v1/profiles/options/projects/(?P<pk_project>[0-9]+)$',
        BusinessViewSets.ProjectProfileOptionsView.as_view()),

    # jobs - lifts
    url(r'^api/v1/jobs/(?P<pk_job>[0-9]+)/lifts/(?P<pk_lift>[0-9]+)$',
        BusinessViewSets.JobLiftRelationView.as_view()),

    # procedures - tasks
    url(r'^api/v1/procedures/(?P<pk_procedure>[0-9]+)/tasks/(?P<pk_task>[0-9]+)$',
        BusinessViewSets.ProcedureTaskRelationView.as_view()),

    # technicians - jobs
    url(r'^api/v1/technicians/(?P<pk_technician>[0-9]+)/getJobs$',
        BusinessViewSets.TechnicianJobsRelationView.as_view()),

    # reports
    url(r'^api/v1/reports/(?P<report_id>[0-9]+)/(?P<model_pk>[0-9]+)/run$',
        ReportsViewSet.ReportsView.as_view()),

    # maintenance
    url(r'^api/v1/maintenances/(?P<pk_lift>[0-9]+)/generate_plan$',
        BusinessViewSets.GenerateMaintenancePlanView.as_view()),

]
