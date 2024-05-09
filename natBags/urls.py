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
# for Media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('news/', views.newsPage, name='news'),
    path('services/', views.services, name='services'),
    path('cart/', views.cartPage, name='cart'),
    path('add-to-cart/<pid>', views.add_to_cart, name='add-to-cart'),
    path('remove-cart-item/<cid>', views.remove_cart, name='remove-cart-item'),
    # path('update-cart-item/<cid>', views.update_cart, name='update-cart-item'),
    path('checkout/', views.checkout, name='checkout'),
    path('productDetail/<productid>',views.singleProduct,name='singleProduct'),
    path('newsDetail/<newsid>',views.singleNews, name='singleNews'),

    path('plus/<int:cid>',views.plus, name='plus'),
    path('minus/<cid>',views.minus, name='minus'),

    # start product review urls
    path('PlaceReview', views.PlaceReview, name='PlaceReview'),
    # end product review urls

    path('verify/<token>',views.verify,name='verify'), 

    path('error',views.error, name='notFound'),

    path('userLogin/',views.login, name='login'),
    path('userRegister/',views.register, name='register'),
    path('userLogout/',views.logout, name='logout'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)