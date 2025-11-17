from rest_framework import generics
from rest_framework.response import Response
#from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, UserSerializer, LoginSerializer
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
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        if  (serializer.is_valid()):
            serializer.save()
            username = request.data.get('username')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({
                    "error" : "User Not found"
                },status = status.HTTP_404_NOT_FOUND)
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
            "errors" : serializer.errors, 
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


class TestTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        user = get_object_or_404(
            User, id=user_id
        )
        print(user)
        email = user.email
        #email = User.objects.get(email=email)
        
        return Response({
            "message": "You have access to this view",
            "email" : email,
        }, status=status.HTTP_200_OK)
    

