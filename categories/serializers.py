from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    expense_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'user', 'expense_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_expense_count(self, obj):
        return obj.expenses.count()
    
    def validate_name(self, value):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            instance = getattr(self, 'instance', None)
            
            if instance:
                if Category.objects.filter(
                    user=user,
                    name=value
                ).exclude(id=instance.id).exists():
                    raise serializers.ValidationError(
                        "This category name already exist"
                    )
            else:
                if Category.objects.filter(user=user, name=value).exists():
                    raise serializers.ValidationError(
                        "You already have a category with this name."
                    )
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        
        return super().create(validated_data)
