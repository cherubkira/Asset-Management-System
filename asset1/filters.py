import django_filters
from django.db.models import Q
from .models import Asset

class AssetFilter(django_filters.FilterSet):
    acquired_date = django_filters.DateFromToRangeFilter()
    q = django_filters.CharFilter(method='search', label='Search')

    class Meta:
        model = Asset
        fields = ['status', 'category', 'location', 'assigned_to', 'q']

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(serial_number__icontains=value) |
            Q(description__icontains=value)
        )
