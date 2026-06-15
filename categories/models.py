from django.db import models
from django.conf import settings
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)
    
    user = models.ForeignKey(
        User, 
        on_delete = models.CASCADE,
        related_name = 'categories'
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        unique_together = ['name', 'user']
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    
    
