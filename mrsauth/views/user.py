from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db.models import Q

from ..models import User
from ..serializers import UsersSerializer
from mrs.utils.response import ResponseHttp

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)

# GET many items


@api_view(['GET'])
def user_list(request):

    try:

        if request.method == 'GET':
            items = list(User.objects.all())
            items_serializer = UsersSerializer(items, many=True)

            return JsonResponse(items_serializer.data, safe=False, status=HTTP_200_OK)

    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)

# Create new user


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_init(request):

    user_data = JSONParser().parse(request)
    user_serializer = UsersSerializer(data=user_data)

    if user_serializer.is_valid():
        user_serializer.save()
        return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET, PUT AND DELETE one item


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):

    try:
        item = User.objects.get(pk=pk)

        if request.method == 'GET':
            item_serializer = UsersSerializer(item)
            return JsonResponse({'result': item_serializer.data, 'error': ''}, status=HTTP_200_OK)

        elif request.method == 'PUT':
            item_data = JSONParser().parse(request)
            item_serializer = UsersSerializer(
                item, data=item_data, partial=True)

            if item_serializer.is_valid():
                item_serializer.save()
                return JsonResponse({'result': item_serializer.data, 'error': ''})

            return JsonResponse(item_serializer.errors, status=HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            item.delete()
            return JsonResponse('User was deleted successfully', safe=False, status=HTTP_204_NO_CONTENT)

    except User.DoesNotExist:
        result = ResponseHttp(error='The user does not exist').result
        return JsonResponse(result, status=HTTP_404_NOT_FOUND)
    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# GET an item by condition
@ api_view(['POST'])
def user_filter(request):
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
