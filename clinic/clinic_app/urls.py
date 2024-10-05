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
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/update-note/', views.update_order_note, name='update_order_note'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),

    path('initialize-payment/', views.initialize_payment, name='initialize_payment'),


    path('make-payment/<int:order_id>/', views.make_payment, name='make_payment'),

    path('payment-callback/', views.payment_callback, name='payment_callback'),

    path('product/<slug:slug>/', views.product_detail, name='product_detail'),


    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.product_list, name='category_products'),
    

    path('products/search/', views.product_list, name='product_search'),

    path('api/search/', views.search_products, name='api_search_products'),


    path('api/orders/', views.OrderList.as_view(), name='order-list'),
    path('api/orders/<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),


    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
    path('policy/', views.policy, name='policy'),


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),

    path('api/products/<str:section>/', views.product_api, name='product_api'),

    #-----------------
    path('app/', views.test_api, name='app'),
    path('api/<path:path>', views.proxy_view, name='proxy'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)