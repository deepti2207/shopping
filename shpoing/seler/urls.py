from seler.views import product_upload,CustomerRegistrationSelerView, seller_product
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . forms import LoginForm
from .views import *

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('product_upload/',product_upload,name='product_upload'),
    path('seller_Registration/',CustomerRegistrationSelerView.as_view(),name='Seller_Registration'),
    path('your_products',seller_product,name='seller_product'),
    path('delete_order/<str:pk>/',delete_order,name='delete_order'),
    # path('update_order/<str:pk>/',update_order,name='update_order'),
    path('update_order/<str:pk>/',update_order,name='update_order'),
    path('customer/<str:pk_test>/',customer, name="customer"),
    path('status_seler_count',status_seler_count,name="status_seler_count"),
    path('Product_detail/<int:pk>?45+36+20product/',Product_detail,name='Product_detail'),
]
