from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets

from mrsauth.serializers import GroupsSerializer, PermissionsSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionsSerializer
