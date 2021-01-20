from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from jwt import ExpiredSignatureError, ExpiredSignature
from rest_framework_jwt.utils import jwt_decode_handler

import jwt
from mrs.utils.singleton import Singleton
from mrsauth.models import User


class ModelAuthentication(ModelBackend):

    def authenticate(self, email, password):

        try:
            user = User.objects.get(nick_name=email)

            if getattr(user, 'statusId', 1) and check_password(password, user.password) is True:
                return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def mrs_decode_handler(token):
    unverified_payload = jwt.decode(token, None, False)
    user = unverified_payload.get('username')

    if TokenBlackList.Instance().is_black_listed(user, token):
        raise ExpiredSignature

    return jwt_decode_handler(token)


@Singleton
class TokenBlackList:
    black_list = []

    def is_black_listed(self, user, token):
        return user + "|" + str(token) in self.black_list

    def add(self, user, token):
        self.black_list.append(user + "|" + str(token))
