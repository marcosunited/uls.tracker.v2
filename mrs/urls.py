"""mrsModel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from mrs.utils.filter import QueryRouter

from mrs.views.ProjectViewSets import *

router = QueryRouter()
router.register(r'projects', ProjectViewSet)  # projects url
router.register(r'contacts', ContactViewSet)  # contacts url
router.register(r'contracts', ContractViewSet)  # contracts url
router.register(r'contractsfrequencies', ContractFrequencyViewSet)  # contractsfrequencies url
router.register(r'jobs', JobViewSet)  # jobs url
router.register(r'rounds', RoundViewSet)  # jobs url
router.register(r'agents', AgentViewSet)  # jobs url
router.register(r'technicians', TechnicianViewSet)  # jobs url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('mrsauth.urls')),

    url(r'^api/v1/', include(router.urls)),
]
