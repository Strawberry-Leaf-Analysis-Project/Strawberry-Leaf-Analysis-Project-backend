from rest_framework import serializers
from .models import PlantsDetail

class PlantsDetailSerializer(serializers.ModelSerializer) :
    class Meta :
        model = PlantsDetail
        fields = '__all__'