
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    #path('api/expenses/', include('exp_tracker.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/categories/', include('categories.urls')),
    #path('api/expenses/', include('expenses.urls')),
]
