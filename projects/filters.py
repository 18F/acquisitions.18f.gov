import django_filters
from projects.models import IAA, Project, AgileBPA, Micropurchase


class AgileBPAFilter(django_filters.rest_framework.FilterSet):
    project_id = django_filters.CharFilter(name="project__id")

    class Meta:
        model = AgileBPA
        fields = ['id', 'name', 'project_id']


class MicropurchaseFilter(django_filters.rest_framework.FilterSet):
    project_id = django_filters.CharFilter(name="project__id")

    class Meta:
        model = Micropurchase
        fields = ['id', 'name', 'project_id']


class ProjectFilter(django_filters.rest_framework.FilterSet):
    iaa_id = django_filters.CharFilter(name="iaa__id")

    class Meta:
        model = Project
        fields = ['id', 'name', 'iaa_id']
