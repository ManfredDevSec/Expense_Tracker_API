from rest_framework import serializers
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=150, write_only=True)
    username = serializers.CharField(max_length=50, min_length=6)
    class Meta:
        model = User
        fields = (
            "id","first_name", "last_name", "email", "username", "password"
        )
    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": ('email already exists')}
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": ('username already exists')}
            )
        return super().validate(args)
        
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username").strip()
        password = data.get("password")

        try:
            user = User.objects.get(
                username=username
            )
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email/username or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email/phone or password.")

        data["user"] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "first_name", "last_name", "email", "username"
        )

