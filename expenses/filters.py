import django_filters
from .models import Expense
from categories.models import Category

class ExpenseFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='date', 
        lookup_expr='gte',
        label='From Date (YYYY-MM-DD)'
    )
    end_date = django_filters.DateFilter(
        field_name='date', 
        lookup_expr='lte',
        label='To Date (YYYY-MM-DD)'
    )
    
    min_amount = django_filters.NumberFilter(
        field_name='amount', 
        lookup_expr='gte',
        label='Minimum Amount'
    )
    max_amount = django_filters.NumberFilter(
        field_name='amount', 
        lookup_expr='lte',
        label='Maximum Amount'
    )
    
    
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Category'
    )
    

    
    description = django_filters.CharFilter(
        field_name='description',
        lookup_expr='icontains',
        label='Description Contains'
    )
    

    year = django_filters.NumberFilter(
        field_name='date__year',
        label='Year'
    )
    month = django_filters.NumberFilter(
        field_name='date__month',
        label='Month (1-12)'
    )

    class Meta:
        model = Expense
        fields = ['category', 'date', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            self.filters['category'].queryset = Category.objects.filter(user=self.request.user)