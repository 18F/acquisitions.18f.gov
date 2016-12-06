import django_filters
from projects.models import IAA, Project, Buy


class BuyFilter(django_filters.rest_framework.FilterSet):
    min_dollars = django_filters.NumberFilter(
        name="dollars",
        lookup_expr='gte',
    )
    max_dollars = django_filters.NumberFilter(
        name="dollars",
        lookup_expr='lte',
    )

    class Meta:
        model = Buy
        # Allowing filtering by project leaks non-public project names in the
        # browseable API, so it cannot be provided here until the browseable
        # API is turned off
        fields = ['id', 'name', 'min_dollars', 'max_dollars']
