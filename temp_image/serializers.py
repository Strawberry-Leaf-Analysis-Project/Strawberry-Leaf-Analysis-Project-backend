from rest_framework import serializers
from .models import TempImage

class TempImageSerializer(serializers.ModelSerializer) :
    class Meta :
        model = TempImage
        fields = '__all__'