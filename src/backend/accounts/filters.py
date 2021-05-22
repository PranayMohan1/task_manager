import django_filters
from django.db.models import Q

from .models import User


class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="custom_search")

    class Meta:
        model = User
        fields = {
            'id': ['exact'],
            'username': ['icontains'],
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'mobile': ['icontains'],
            'email': ['icontains']
        }

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(username__icontains=value) | Q(
                mobile__icontains=value) | Q(email__icontains=value))
