from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Category
from .serializers import CategorySerializer
from .permissions import IsCategoryOwner
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsCategoryOwner, IsAuthenticated]
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)\
                             .select_related('user')\
                             .prefetch_related('expenses')\
                             .annotate(expense_count=Count('expenses'))
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def with_expenses(self, request):
        categories = self.get_queryset().filter(expenses__isnull=False).distinct()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def without_expenses(self, request):
        """
        Custom endpoint to get categories with no expenses
        """
        categories = self.get_queryset().filter(expenses__isnull=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)