"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import  Login, GoogleLogin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include("users.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/login/', Login.as_view(), name='login_using_password'),
    path('api/google_login/', GoogleLogin.as_view(), name='login_using_gooogle'),
    path('api/posts/', include('posts.urls')),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
