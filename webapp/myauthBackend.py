from django.contrib.auth.backends import BaseBackend

from .models import Users


class UserAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        """
        Overrides the authenticate method to allow users to log in using their email address.
        """
        try:
            user = Users.objects.get(username=username)
            if user:
                return user
            return None
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
