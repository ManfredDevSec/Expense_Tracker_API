from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta
from .models import Expense
from .serializers import ExpenseSerializer
from .permissions import IsExpenseOwner
from .filters import ExpenseFilter


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsExpenseOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter
    
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)\
                            .select_related('category', 'user')\
                            .order_by('-date', '-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.get_queryset()
        
        total_expenses = queryset.aggregate(
            total=Sum('amount'),
            average=Avg('amount'),
            count=Count('id')
        )
        
        category_breakdown = queryset.values(
            'category__name'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        return Response({
            'summary': total_expenses,
            'by_category': list(category_breakdown)
        })
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_expenses = self.get_queryset().filter(date__gte=thirty_days_ago)
        
        page = self.paginate_queryset(recent_expenses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(recent_expenses, many=True)
        return Response(serializer.data)

