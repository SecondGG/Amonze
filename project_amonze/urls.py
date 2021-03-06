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
from django.urls import path, include
from app_amonze import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name = 'home'),
    path('marketplace', views.marketplace, name  = 'marketplace'),
    path('item/<int:item_id>', views.item,  name = 'item'),
    path('admin/', admin.site.urls),
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('signup/', views.signup, name = 'signup'),
    path('profile/', views.profile, name = 'profile'),
    path('accounts/', include('allauth.urls')),
    path('cart/', views.cart, name ='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('owned/', views.owned, name = 'owned'),
    path('eth_pay/', views.eth_pay, name='eth_pay'),
    path('accounts/profile/', views.profile, name = 'profile'),
    path('qr_mobile/<mobile>/<amount>/qr.png', views.get_qr, name='qr'),
    path('qr_nid/<nid>/<amount>/', views.get_qr, name='qr'),
    path('checkout/promptpay/', views.promptpay, name= 'promptpay')
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)