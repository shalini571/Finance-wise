from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),  # Add this line for base.html
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('validate-username/', views.validate_username, name='validate-username'),
    path('validate-email/', views.validate_email, name='validate-email'),
    
    # Password Reset URLs
    path('reset-password/', views.reset_password_view, name='password_reset'),
    path('reset-password-sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name='authentication/password-reset-sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='authentication/set-new-password.html'),
         name='password_reset_confirm'),
    path('reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password-reset-complete.html'),
         name='password_reset_complete'),
]