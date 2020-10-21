import jwt

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
from mrsauth.models import Console, UsersHistoryLogin
from mrsauth.serializers import UsersSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def do_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user_agent = request.META.get('HTTP_USER_AGENT')

    if username is None or password is None:
        return JsonResponse('Please provide both username and password', safe=False,
                            status=HTTP_400_BAD_REQUEST)

    user = ModelAuthentication.authenticate(
        request, username=username, password=password)

    if not user:
        return JsonResponse('User or password wrong', safe=False,
                            status=HTTP_404_NOT_FOUND)

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

    response = {"user": user_serializer.data, "token": token}

    response = ObjectResponse(response, None)

    return Response(response.result,
                    status=HTTP_200_OK)
