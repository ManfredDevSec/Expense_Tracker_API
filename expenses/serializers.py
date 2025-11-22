from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Expense
from categories.models import Category
User = get_user_model()



class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'date', 'category', 'category_name',
            'description', 'user', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'category_name']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
        
    def validate_category(self, value):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if value.user != request.user:
                raise serializers.ValidationError("You can only use your own categories.")
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
