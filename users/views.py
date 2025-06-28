from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import secrets
import string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Utilisateur créé avec succès',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Connexion réussie',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = CustomUser.objects.get(email=email)
        
        # Générer un token de récupération
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        user.reset_password_token = token
        user.reset_password_expires = timezone.now() + timedelta(hours=24)
        user.save()
        
        # Envoyer l'email (pour le développement, affiché dans la console)
        reset_url = f"http://localhost:3000/reset-password?token={token}"
        
        # En production, utilisez un template HTML
        subject = 'Réinitialisation de votre mot de passe'
        message = f"""
        Bonjour {user.first_name},
        
        Vous avez demandé la réinitialisation de votre mot de passe.
        Cliquez sur le lien suivant pour définir un nouveau mot de passe :
        
        {reset_url}
        
        Ce lien expire dans 24 heures.
        
        Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.
        
        Cordialement,
        L'équipe SpaceHack
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return Response({
            'message': 'Un email de réinitialisation a été envoyé à votre adresse email.'
        })

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            user = CustomUser.objects.get(
                reset_password_token=token,
                reset_password_expires__gt=timezone.now()
            )
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'Token invalide ou expiré.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mettre à jour le mot de passe
        user.set_password(new_password)
        user.reset_password_token = None
        user.reset_password_expires = None
        user.save()
        
        return Response({
            'message': 'Mot de passe mis à jour avec succès.'
        })

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        new_password = serializer.validated_data['new_password']
        
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Mot de passe modifié avec succès.'
        })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        print(refresh_token)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Déconnexion réussie"})
    except Exception as e:
        print(e)
        return Response({"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_info(request):
    """Endpoint pour récupérer les informations de l'utilisateur connecté"""
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)
