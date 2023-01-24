from rest_framework import serializers
from .models import PlantsGroup

class PlantsGroupSerializer(serializers.ModelSerializer) :
    class Meta :
        model = PlantsGroup
        fields = '__all__'