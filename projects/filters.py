import django_filters
from projects.models import IAA, Project, Buy


class BuyFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Buy
        fields = ['id', 'name', 'project__id']


class ProjectFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Project
        fields = ['id', 'name', 'iaa__id']
