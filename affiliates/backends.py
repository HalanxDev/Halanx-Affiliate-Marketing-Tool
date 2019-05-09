from django.contrib.auth import get_user_model  # gets the user_model django  default or your own custom
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            user = UserModel.objects.filter(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            ).distinct()
        except UserModel.DoesNotExist:
            return None

        if user.exists():
            user_obj = user.first()
            if user_obj.check_password(password):
                return user_obj
            return None
        else:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
