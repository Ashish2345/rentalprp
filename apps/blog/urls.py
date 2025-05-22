from django.urls import path, include
from .import views

urlpatterns = [
    path('chat/', include('chatbot.urls')),
    path('', views.PostList.as_view(), name='blog'),
    path('<slug:slug>/', views.DetailView.as_view(), name="blog_detail"),
]