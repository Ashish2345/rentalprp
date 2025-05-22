from django.urls import path
from . import views


#urlpatterns for app cart
urlpatterns = [
    path('', views.orders, name='my-orders'),

]