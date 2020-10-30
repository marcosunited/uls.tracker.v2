"""
mrs URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from mrs.utils.filter import QueryRouter, ModelMetaView

from mrs.views.ProjectViewSets import *

router = QueryRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'contractsfrequencies', ContractFrequencyViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'rounds', RoundViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'technicians', TechnicianViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('mrsauth.urls')),
    url(r'^api/v1/meta/(?P<model>\D+)/', ModelMetaView.as_view()),
    url(r'^api/v1/', include(router.urls)),
]
