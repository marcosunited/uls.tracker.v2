from typing import TypeVar

from django.contrib.auth.models import Group, Permission

from mrs.models import Profile
from mrsauth.serializers import GroupsSerializer, PermissionsSerializer, ProfilesSerializer
from mrs.utils.cache import CachedModelViewSet
from mrs.utils.filter import FilteredModelViewSet


class GroupViewSet(FilteredModelViewSet):
    # queryset = Group.objects.all()
    serializer_class = GroupsSerializer

    class Meta:
        model = Group


class PermissionViewSet(CachedModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionsSerializer


class ProfileViewSet(CachedModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfilesSerializer
