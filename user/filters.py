# from django_filters import FilterSet, filters
from .models import CustomUser
import django_filters


class UserFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(lookup_expr="exact")
    email = django_filters.CharFilter(lookup_expr="icontains")
    first_name = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")
    full_name = django_filters.CharFilter(lookup_expr="icontains")
    is_active = django_filters.BooleanFilter(lookup_expr="exact")
    is_staff = django_filters.BooleanFilter(lookup_expr="exact")
    role = django_filters.CharFilter(field_name="role__name", lookup_expr="icontains")
    country = django_filters.NumberFilter(lookup_expr="exact")
    page_size = django_filters.NumberFilter(lookup_expr="exact")

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "full_name",
            "email",
            "is_active",
            "is_staff",
            "role",
            "country",
        ]
