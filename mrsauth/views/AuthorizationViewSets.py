from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets

from mrs.models import Profile
from mrsauth.serializers import GroupsSerializer, PermissionsSerializer, ProfilesSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionsSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfilesSerializer
