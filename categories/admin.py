from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'expense_count', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def expense_count(self, obj):
        return obj.expenses.count()
    expense_count.short_description = 'Expense Count'