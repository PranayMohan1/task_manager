from ..base.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.decorators import action
from django.contrib.auth import logout, get_user_model
from ..base.services import auth_register_user, auth_login
from rest_framework import response
from .models import AuthTokenModel


from .serializers import UserSerializer
from .filters import UserFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(ModelViewSet):
    """
    Here we have user login, logout, endpoints.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    parser_classes = (JSONParser, MultiPartParser)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = UserFilter
        queryset = self.filter_queryset(queryset)
        return queryset

    @action(detail=False, methods=['POST', 'GET'])
    def register(self, request):
        data = auth_register_user(request)
        return response.Response(data)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        return auth_login(request)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        if request.user.is_authenticated:
            AuthTokenModel.objects.filter(user=request.user).delete()
            logout(request)
            return response.Response({"detail": "Successfully logged out."})
        else:
            return response.Response({"detail": "Wrong user"})
