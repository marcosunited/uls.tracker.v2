import jwt
from django.contrib.auth import logout

from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED

)
from rest_framework_jwt.utils import jwt_decode_handler

from mrsauth.backend import ModelAuthentication, TokenBlackList
from mrs import settings
from mrs.utils.response import ResponseHttp as ObjectResponse
from mrsauth.models import Console, UsersHistoryLogin
from mrsauth.serializers import UsersSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def do_login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user_agent = request.META.get('HTTP_USER_AGENT')

    if email is None or password is None:
        response = ObjectResponse(None, 'Please provide both email and password')
        return Response(response.result, status=HTTP_400_BAD_REQUEST)

    try:
        validate_email(email)
    except ValidationError:
        response = ObjectResponse(None, 'Invalid email, please provide a valid email')
        return Response(response.result, status=HTTP_400_BAD_REQUEST)

    user = ModelAuthentication.authenticate(
        request, email=email, password=password)

    if not user:
        response = ObjectResponse(None, 'User or password is wrong')
        return Response(response.result, status=HTTP_401_UNAUTHORIZED)

    # log to login history
    console = Console.objects.get(id=1)
    login_history = UsersHistoryLogin(user=user,
                                      console=console,
                                      user_agent=user_agent)
    login_history.save()

    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)

    user_logged_in.send(sender=user.__class__,
                        request=request, user=user)

    user_serializer = UsersSerializer(user)

    r = user_serializer.data
    r["email"] = r["nick_name"]
    r.pop("nick_name")

    response = {"user": r, "token": token}

    response = ObjectResponse(response, None)

    return Response(response.result, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def do_logout(request):
    try:
        user = str(request.user)
        token = request.auth
        TokenBlackList.Instance().add(user, token)
        logout(request)
        return Response({'result': 'OK', 'error': ""}, status=HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

