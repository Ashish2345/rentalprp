from django.urls import path
from django.contrib.auth import views as auth_views
from .import views
urlpatterns = [
    path('', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify-email'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_customer, name='edit_profile'),
    path('create_profile/', views.create_profile, name='create_profile'),  # New URL for profile creation
    path('add_property/', views.add_property, name='add_property'),
    path('edit-property/<int:pk>/', views.edit_property, name='edit_property'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]