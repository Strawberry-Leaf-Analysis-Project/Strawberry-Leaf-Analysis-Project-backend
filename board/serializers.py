from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer) :
    user=serializers.ReadOnlyField(source = 'user.id')
    class Meta :
        model = Board
        fields = '__all__'