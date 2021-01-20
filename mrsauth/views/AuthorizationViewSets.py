from django.contrib.auth.models import Group, Permission
from django.http import JsonResponse
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from mrs.models import Profile
from mrs.utils.response import ResponseHttp
from mrsauth.serializers import GroupsSerializer, PermissionsSerializer, ProfilesSerializer
from mrs.utils.cache import CachedModelViewSet
from mrs.utils.filter import FilteredModelViewSet


class GroupViewSet(FilteredModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer

    class Meta:
        model = Group


class GroupUserRelationView(APIView):
    def post(self, request, pk_group, pk_user):
        try:
            group = Group.objects.get(id=pk_group)
            group.user_set.add(pk_user)
            group_serializer = GroupsSerializer(group)
            return JsonResponse({'result': group_serializer.data, 'error': ''})
        except Group.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The group does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk_group, pk_user):
        try:
            group = Group.objects.get(id=pk_group)
            group.user_set.remove(pk_user)
            group_serializer = GroupsSerializer(group)
            return JsonResponse({'result': group_serializer.data, 'error': ''})
        except Group.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The group does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


class PermissionViewSet(CachedModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionsSerializer


class ProfileViewSet(CachedModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfilesSerializer
