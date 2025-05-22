from django.urls import path
from .import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('notification/view/<int:id>/', views.view_notifications, name='view_notification'),
]