from django.urls import path
from . import views


#urlpatterns for app cart
urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('success/', views.success, name='success'),

   path('initiate-khalti/', views.initiate_khalti_payment, name='initiate-khalti'),
    path('payment/success/', views.verify_khalti_payment, name='khalti-success'),
]