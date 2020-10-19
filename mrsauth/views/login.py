import jwt

from datetime import timedelta

from django.contrib.auth.signals import user_logged_in
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from mrsauth.backend import ModelAuthentication
from mrs import settings
from mrs.utils.response import ResponseHttp as ObjectResponse


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def do_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return JsonResponse('Please provide both username and password', safe=False,
                            status=HTTP_400_BAD_REQUEST)

    user = ModelAuthentication.authenticate(
        request, username=username, password=password)

    if not user:
        return JsonResponse('User or password wrong', safe=False,
                            status=HTTP_404_NOT_FOUND)

    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    user_logged_in.send(sender=user.__class__,
                        request=request, user=user)

    response = {
        "id": user.id,
        "username": user.nick_name,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "statusId": user.statusId,
        "salt": user.salt,
        "token": token,
        "lastlogin": user.last_login,
        "expiration": user.last_login + timedelta(minutes=30)
    }

    response = ObjectResponse(response, None)

    return Response(response.result,
                    status=HTTP_200_OK)
