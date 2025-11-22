import django_filters
from .models import Expense

class ExpenseFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    
    class Meta:
        model = Expense
        fields = ['category', 'date']