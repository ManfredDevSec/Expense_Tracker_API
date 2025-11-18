from rest_framework import generics
from rest_framework.response import Response
#from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, LoginSerializer,UserProfileSerializer,ChangePasswordSerializer
from rest_framework import permissions
import uuid
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        if  (serializer.is_valid()):
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            
            return Response({
                "RequestId": str(uuid.uuid4()),
                "message" : "User created successfully",
                "user" : serializer.data,
                "access" : access,
                "refresh": str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response({
            "error" : serializer.errors, 
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        #serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "error" : serializer.errors,
        }, status = status.HTTP_400_BAD_REQUEST)

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
  

