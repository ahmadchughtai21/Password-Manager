"""
URL configuration for password_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from password_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.authentication, name='authentication'),
    path('home/', views.home, name='home'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('save_password/', views.save_password, name='save_password'),
    path('generate_password/', views.generate_password, name='generate_password'),
    path('view_passwords/', views.view_passwords, name='view_passwords'),
    path('delete_password/', views.delete_password, name='delete_password'),
    path('change_master_password/', views.change_master_password, name='change_master_password'),
    path('copy_password/', views.copy_password, name='copy_password'),


    # path("__reload__/", include("django_browser_reload.urls")),
]
