from rest_framework.authentication import TokenAuthentication

from ..accounts.models import AuthTokenModel


class TaskManagerTokenAuthentication(TokenAuthentication):
    model = AuthTokenModel
