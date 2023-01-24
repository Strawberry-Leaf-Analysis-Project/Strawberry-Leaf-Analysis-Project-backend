from rest_framework import serializers
from .models import PlantsByDisease

class PlantsDiseaseSerializer(serializers.ModelSerializer) :
    class Meta :
        model = PlantsByDisease
        fields = '__all__'