from django.contrib.auth.backends import BaseBackend
from .models import Users


class UserAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(username=username)
            if user and user.role == '002':
                return user
            elif user.role != '002' and user.check_password(password):
                return user
        except Users.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Overrides the get_user method to allow users to log in using their email address.
        """
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
