from django.urls import path
from .views import (
    RegistrationAPIView, LoginAPIView,
    UserProfileAPIView,ChangePasswordAPIView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('token-pair/', TokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    #path('test/<uuid:user_id>/', TestTokenView.as_view(), name='test'),
    
]



