"""
URL configuration for clinic project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/update-note/', views.update_order_note, name='update_order_note'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),

    path('initialize-payment/', views.initialize_payment, name='initialize_payment'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),

    path('product/<slug:slug>/', views.product_detail, name='product_detail'),


    #path('category', views.category, name='category'),


    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.product_list, name='category_products'),
    

    path('products/search/', views.product_list, name='product_search'),

    path('api/search/', views.search_products, name='api_search_products'),


    path('api/orders/', views.OrderList.as_view(), name='order-list'),
    path('api/orders/<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)