from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('<slug:category_slug>/<slug:property_slug>/', views.property, name='property'),
    path('<slug:category_slug>/', views.category, name='category'),
]