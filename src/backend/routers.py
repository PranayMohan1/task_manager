from rest_framework.routers import DefaultRouter
from .accounts.viewsets import UserViewSet
from .task_manager.viewsets import ProjectsViewSet

restricted_router = DefaultRouter()

restricted_router.register(r'users', UserViewSet)
restricted_router.register(r'projects', ProjectsViewSet)