"""
mrs URL Configuration
"""
import sys, inspect

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path

from mrs.rules.RulesViewSet import RulesViewSet
from mrs.rules.rules import RulesMetaView
from mrs.utils.storage import FileView
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
router.register(r'rules', RulesViewSet)


"""
# dynamic views setup
for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and obj.__name__.endswith('Serializer'):
        class_name = obj.__name__[0:obj.__name__.index('Serializer')]
        view_class = type(class_name,
                          (FilteredModelViewSet,),
                          {'queryset': Job.objects.all(),
                           'serializer_class': JobsSerializer})
        router.register(class_name.lower(), view_class)
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('mrsauth.urls')),
    url(r'^api/v1/meta/(?P<model>\D+)/', ModelMetaView.as_view()),
    url(r'^api/v1/rules/meta/(?P<model>\D+)/', RulesMetaView.as_view()),
    url(r'^api/v1/upload/$', FileView.as_view(), name='file-upload'),
    url(r'^api/v1/', include(router.urls)),
]
