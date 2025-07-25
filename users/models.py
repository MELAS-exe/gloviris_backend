from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Champs pour la récupération de mot de passe
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    reset_password_expires = models.DateTimeField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

from django.db import models
from django.contrib.auth import get_user_model
from .models import CustomUser

class PlantAnalysis(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='plant_analyses')
    species = models.CharField(max_length=100)
    disease = models.CharField(max_length=100)
    status = models.CharField(max_length=200)
    confidence = models.FloatField(default=0.0)
    image_path = models.CharField(max_length=500)
    is_healthy = models.BooleanField(default=True)
    class_name = models.CharField(max_length=100, default='')
    matched_plant_id = models.IntegerField(null=True, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-analyzed_at']
        verbose_name = 'Plant Analysis'
        verbose_name_plural = 'Plant Analyses'
    
    def __str__(self):
        return f"{self.species} - {self.disease} ({self.analyzed_at.strftime('%Y-%m-%d')})"