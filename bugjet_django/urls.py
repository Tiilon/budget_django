"""bugjet_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api import urls as api_urls
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt import views as jwt_views
from user.views import *

schema_view = get_swagger_view(title="News Contents API")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_create'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
