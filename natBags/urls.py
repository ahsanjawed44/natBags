
from django.contrib import admin
from django.urls import path
from natBags import views

# for Media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    # Static Page URLs
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    
    # Shop URLs
    path('shop/', views.shop, name='shop'),
    path('productDetail/<productid>',views.singleProduct,name='singleProduct'),
    path('search/', views.search, name='search'),
    path('PlaceReview', views.PlaceReview, name='PlaceReview'),

    # News URLs
    path('news/', views.newsPage, name='news'),
    path('newsDetail/<newsid>',views.singleNews, name='singleNews'),

    # Cart URLs
    path('cart/', views.cartPage, name='cart'),
    path('add-to-cart/<pid>', views.add_to_cart, name='add-to-cart'),
    path('remove-cart-item/<cid>', views.remove_cart, name='remove-cart-item'),
    path('plus/<int:cid>',views.plus, name='plus'),
    path('minus/<cid>',views.minus, name='minus'),

    # Ordering URLs
    path('checkout/', views.checkout, name='checkout'),
    path('order/',views.order,name='order'),

    # Email verification URLS
    path('verifyOrder/<token>',views.verifyOrder,name='verifyOrder'), 
    path('verifyCustomer/<token>',views.verifyCustomer,name='verifyCustomer'), 

    # Authentication URLs
    path('userLogin/',views.login, name='login'),
    path('userRegister/',views.register, name='register'),
    path('userLogout/',views.logout, name='logout'),
    
    # ERROR URL
    path('error',views.error, name='notFound'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)