import django_filters
from .models import university

class UniversityFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='country__name', lookup_expr='icontains')
    available_courses = django_filters.CharFilter(field_name='available_courses__course_name', lookup_expr='icontains')
    degree = django_filters.CharFilter(field_name='degree__degree', lookup_expr='icontains')

    class Meta:
        model = university
        fields = ['country', 'available_courses', 'degree']
