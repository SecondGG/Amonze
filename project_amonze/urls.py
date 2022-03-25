"""project_amonze URL Configuration

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
from unicodedata import name
from django.contrib import admin
from django.urls import path
from mysqlx import View
from app_amonze import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('marketplace', views.marketplace, name  = 'marketplace'),
    path('item/<int:item_id>', views.item,  name = 'item'),
    path('admin/', admin.site.urls),
    path('register', View.register, name = 'register'),
    path('register_detail', View.register_detail, name = 'register_detail'),

]
