from rest_framework import serializers
from .models import soil, plant

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = plant
        fields = ['id', 'name', 'image', 'description']

class SoilSerializer(serializers.ModelSerializer):
    plants = PlantSerializer(many=True, read_only=True)
    
    class Meta:
        model = soil
        fields = ['id', 'name', 'image', 'description', 'plants']

class PlantListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des plantes avec un aperçu des sols compatibles"""
    soils_count = serializers.SerializerMethodField()
    
    class Meta:
        model = plant
        fields = ['id', 'name', 'image', 'description', 'soils_count']
    
    def get_soils_count(self, obj):
        return obj.soils.count()

class SoilListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des sols avec un aperçu des plantes cultivables"""
    plants_count = serializers.SerializerMethodField()
    
    class Meta:
        model = soil
        fields = ['id', 'name', 'image', 'description', 'plants_count']
    
    def get_plants_count(self, obj):
        return obj.plants.count() 