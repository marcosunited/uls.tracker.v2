from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

from mrsauth.models import User


class ModelAuthentication(ModelBackend):

    def authenticate(self, username, password):

        try:
            user = User.objects.get(nick_name=username)

            if getattr(user, 'statusId', 1) and check_password(password, user.password) is True:
                return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
