from rest_framework import serializers
from .models import BoardLikeByUser

class BoardLikeByUserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = BoardLikeByUser
        fields = '__all__'