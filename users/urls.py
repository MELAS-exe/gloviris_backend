from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # Authentification
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profil utilisateur
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('user-info/', views.user_info, name='user_info'),
    
    # Gestion des mots de passe
    path('password/reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/change/', views.ChangePasswordView.as_view(), name='change_password'),
] 