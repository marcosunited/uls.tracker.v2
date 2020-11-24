from django.contrib.auth.models import Group
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Q

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView

from ..models import User
from ..serializers import UsersSerializer, GroupsSerializer
from mrs.utils.response import ResponseHttp

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)


class UserList(APIView):

    # GET many items

    def get(self, request):
        try:
            items = list(User.objects.all())
            items_serializer = UsersSerializer(items, many=True)

            return JsonResponse(items_serializer.data, safe=False, status=HTTP_200_OK)

        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserInit(APIView):

    # Create new user

    def post(self, request):
        user_data = JSONParser().parse(request)
        user_serializer = UsersSerializer(data=user_data)

        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET, PUT AND DELETE one item
class UserDetail(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user_serializer = UsersSerializer(user)
            return JsonResponse({'result': user_serializer.data, 'error': ''}, status=HTTP_200_OK)

        except User.DoesNotExist:
            result = ResponseHttp(error='The user does not exist').result
            return JsonResponse(result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user_data = JSONParser().parse(request)
            user_serializer = UsersSerializer(
                user, data=user_data, partial=True)

            if 'add_to' in user_data:
                for _group in user_data["add_to"]:
                    group = Group.objects.get(name=_group)
                    group.user_set.add(user.id)

            if 'remove_from' in user_data:
                for _group in user_data["remove_from"]:
                    group = Group.objects.get(name=_group)
                    group.user_set.remove(user.id)

            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse({'result': user_serializer.data, 'error': ''})

            return JsonResponse(user_serializer.errors, status=HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            result = ResponseHttp(error='The user does not exist').result
            return JsonResponse(result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return JsonResponse('User was deleted successfully', safe=False, status=HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            result = ResponseHttp(error='The user does not exist').result
            return JsonResponse(result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# GET an item by condition
class UserFilter(APIView):
    def post(self, request):
        items = list(User.objects.filter(Q(firstName__icontains=request.data.get(
            'firstName')) | Q(lastName__icontains=request.data.get('lastName'))
                                         | Q(nick_name__icontains=request.data.get('nick_name'))))

        try:
            if request.method == 'POST':
                item_serializer = UsersSerializer(items, many=True)
                return JsonResponse(item_serializer.data, safe=False)

        except User.DoesNotExist:
            return JsonResponse(ResponseHttp(error='The item does not exist').result, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


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
