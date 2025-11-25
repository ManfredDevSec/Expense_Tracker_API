from rest_framework import generics,status, serializers
from rest_framework.response import Response
#from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, LoginSerializer,UserProfileSerializer,ChangePasswordSerializer
from rest_framework import permissions
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()

import logging

logger = logging.getLogger('django')

class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            logger.info(f"New user registered: {user.username} ({user.email})")
            
            return Response({
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            logger.info(f"User logged in: {user.username}")
            
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        

        username = request.data.get('username', 'unknown')
        logger.warning(f"Failed login attempt for username: {username}")
        
        return Response({
            "error": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)                

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user
    
class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = self.request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"error": "Wrong old password"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
      
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({"message": "Password updated successfully"}) 
  

