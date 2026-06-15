from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['amount', 'category', 'user', 'date', 'created_at']
    list_filter = ['category', 'user', 'date', 'created_at']
    search_fields = ['description', 'category__name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    list_per_page = 25