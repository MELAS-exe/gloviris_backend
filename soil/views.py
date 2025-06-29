from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

from .models import soil, plant
from .serializers import (
    PlantSerializer, 
    SoilSerializer, 
    PlantListSerializer, 
    SoilListSerializer
)

class PlantListView(generics.ListAPIView):
    """
    API endpoint pour lister toutes les plantes
    GET /api/plants/
    """
    queryset = plant.objects.all()
    serializer_class = PlantListSerializer
    permission_classes = [permissions.AllowAny]

class PlantDetailView(generics.RetrieveAPIView):
    """
    API endpoint pour récupérer les détails d'une plante spécifique
    GET /api/plants/{id}/
    """
    queryset = plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [permissions.AllowAny]

class SoilListView(generics.ListAPIView):
    """
    API endpoint pour lister tous les sols
    GET /api/soils/
    """
    queryset = soil.objects.all()
    serializer_class = SoilListSerializer
    permission_classes = [permissions.AllowAny]

class SoilDetailView(generics.RetrieveAPIView):
    """
    API endpoint pour récupérer les détails d'un sol spécifique
    GET /api/soils/{id}/
    """
    queryset = soil.objects.all()
    serializer_class = SoilSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def plants_by_soil(request, soil_id):
    """
    API endpoint pour récupérer toutes les plantes cultivables dans un sol spécifique
    GET /api/soils/{soil_id}/plants/
    """
    soil_obj = get_object_or_404(soil, id=soil_id)
    plants = soil_obj.plants.all()
    serializer = PlantSerializer(plants, many=True)
    
    return Response({
        'soil': {
            'id': soil_obj.id,
            'name': soil_obj.name
        },
        'plants': serializer.data,
        'count': plants.count()
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def soils_by_plant(request, plant_id):
    """
    API endpoint pour récupérer tous les sols compatibles pour une plante spécifique
    GET /api/plants/{plant_id}/soils/
    """
    plant_obj = get_object_or_404(plant, id=plant_id)
    soils = plant_obj.soils.all()
    serializer = SoilListSerializer(soils, many=True)
    
    return Response({
        'plant': {
            'id': plant_obj.id,
            'name': plant_obj.name
        },
        'soils': serializer.data,
        'count': soils.count()
    })
