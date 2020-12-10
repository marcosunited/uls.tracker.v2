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


router = QueryRouter()

router.register(r'meta_types', MetadataTypeViewSet)
router.register(r'meta_values', MetadataValuesViewSet)

router.register(r'projects', ProjectViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'contractsfrequencies', ContractFrequencyViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'rounds', RoundViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'technicians', TechnicianViewSet)
router.register(r'lifts', LiftViewSet)
router.register(r'notes', NoteViewSet)

router.register(r'rules', RulesViewSet)

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
    url(r'^api/v1/rounds/(?P<pk_round>[0-9]+)/technician/(?P<pk_technician>[0-9]+)$',
        BusinessViewSets.RoundTechnicianRelationView.as_view()),

    # technicians - jobs
    url(r'^api/v1/technicians/(?P<pk_technician>[0-9]+)/getJobs$',
        BusinessViewSets.TechnicianJobsRelationView.as_view()),

    # reports
    url(r'^api/v1/reports/(?P<report_id>[0-9]+)/(?P<model_pk>[0-9]+)/run$',
        ReportsViewSet.ReportsView.as_view()),


]
