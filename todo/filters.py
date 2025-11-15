import django_filters
from django_filters import FilterSet
from .models import Todo


class TodoFilter(FilterSet):
    title_search = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains"
    )
    description_search = django_filters.CharFilter(
        field_name="description", lookup_expr="icontains"
    )

    class Meta:
        model = Todo
        fields = ["title_search", "description_search", "completed", "date_created"]
