from django.db import models
from django.utils import timezone
from categories.models import Category
from django.conf import settings
import uuid

class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)  
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='expenses'  
        )
    description = models.TextField(blank=True, null=True, max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='expenses' 
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'category']),
        ]
    
    def __str__(self):
        return f"{self.amount} - {self.category.name} ({self.date})"
    
    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)

