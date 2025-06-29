from django.urls import path
from . import views

app_name = 'soil'

urlpatterns = [
    # Endpoints pour les plantes
    path('plants/', views.PlantListView.as_view(), name='plant_list'),
    path('plants/<int:pk>/', views.PlantDetailView.as_view(), name='plant_detail'),
    
    # Endpoints pour les sols
    path('soils/', views.SoilListView.as_view(), name='soil_list'),
    path('soils/<int:pk>/', views.SoilDetailView.as_view(), name='soil_detail'),
    
    # Endpoints pour les relations
    path('soils/<int:soil_id>/plants/', views.plants_by_soil, name='plants_by_soil'),
    path('plants/<int:plant_id>/soils/', views.soils_by_plant, name='soils_by_plant'),
] 