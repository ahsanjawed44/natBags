"""
URL configuration for natBags project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from natBags import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('news/', views.news, name='news'),
    path('services/', views.services, name='services'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('singleProduct/',views.singleProduct,name='singleProduct'),
    path('singleNews/',views.singleNews, name='singleNews'),
    path('error',views.error, name='notFound'),

    path('userLogin/',views.login, name='login'),
    path('userRegister/',views.register, name='register'),
    path('userLogout/',views.logout, name='logout'),
    
]