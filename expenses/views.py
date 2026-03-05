import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Q, Sum, Avg, Count, Min, Max
from django.utils import timezone
from datetime import timedelta
from .models import Expense
from .serializers import ExpenseSerializer
from .permissions import IsExpenseOwner
from .filters import ExpenseFilter
from categories.models import Category


logger = logging.getLogger('django')

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsExpenseOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ExpenseFilter
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']  
    
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)\
                            .select_related('category', 'user')\
                            .order_by('-date', '-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info(f"User {self.request.user.username} created expense: {serializer.instance.amount}")
    
    def destroy(self, request, *args, **kwargs):
        expense = self.get_object()
        
        logger.info(f"User {request.user.username} deleted expense: {expense.amount}")
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        user_categories = Category.objects.filter(user=request.user)
        category_options = [{'id': cat.id, 'name': cat.name} for cat in user_categories]
        
        date_range = Expense.objects.filter(user=request.user).aggregate(
            min_date=Min('date'),
            max_date=Max('date')
        )
        
        amount_range = Expense.objects.filter(user=request.user).aggregate(
            min_amount=Min('amount'),
            max_amount=Max('amount')
        )
        

        logger.info(f"User {request.user.username} requested filter options")
        
        return Response({
            'categories': category_options,
            'date_range': date_range,
            'amount_range': amount_range
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        stats = queryset.aggregate(
            total=Sum('amount'),
            average=Avg('amount'),
            count=Count('id'),
            highest=Max('amount'),
            lowest=Min('amount')
        )
        
        category_breakdown = queryset.values(
            'category__id', 'category__name'
        ).annotate(
            total=Sum('amount'),
            count=Count('id'),
            average=Avg('amount')
        ).order_by('-total')
        
        monthly_breakdown = []
        today = timezone.now().date()
        
        for i in range(6):
            month_date = today - timedelta(days=30*i)
            year = month_date.year
            month = month_date.month
            
            month_expenses = queryset.filter(
                date__year=year,
                date__month=month
            ).aggregate(
                total=Sum('amount'),
                count=Count('id')
            )
            
            if month_expenses['total'] is not None:
                monthly_breakdown.append({
                    'year': year,
                    'month': month,
                    'month_name': month_date.strftime('%B'),
                    'total': month_expenses['total'],
                    'count': month_expenses['count']
                })
        
        monthly_breakdown.reverse()

        logger.info(f"User {request.user.username} generated summary - Total: {stats['total']}")
        
        return Response({
            'summary': stats,
            'by_category': list(category_breakdown),
            'monthly_trend': monthly_breakdown,
            'filtered_count': queryset.count()
        })

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Search query parameter "q" is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
        
        queryset = self.filter_queryset(queryset)
        
        serializer = self.get_serializer(queryset, many=True)
        
        logger.info(f"User {request.user.username} searched for '{query}' - Found {queryset.count()} results")
        
        return Response({
            'query': query,
            'results': serializer.data,
            'count': queryset.count()
        })      
        