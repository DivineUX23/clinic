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
    #path('cart', views.cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/update-note/', views.update_order_note, name='update_order_note'),


    path('initialize-payment/', views.initialize_payment, name='initialize_payment'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
    #path('payment-success/', views.payment_success, name='payment_success'),
    #path('payment-failed/', views.payment_failed, name='payment_failed'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
