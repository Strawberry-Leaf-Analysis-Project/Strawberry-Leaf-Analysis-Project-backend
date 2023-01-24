from board.models import Board
from disease.models import Disease
from plants_by_disease.models import PlantsByDisease

from plants_group.models import PlantsGroup
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
from .serializers import PlantsDiseaseSerializer
from rest_framework import viewsets,status
from rest_framework.decorators import action

class PlantsByDiseaseListAPI(viewsets.ModelViewSet):
    queryset = PlantsByDisease.objects.all()
    serializer_class = PlantsDiseaseSerializer

    #필요값:board_id:게시판의 id,disease_name:질병명
    #[post] /plants_by_detail/
    def perform_create(self, serializer):
        board=Board.objects.get(id=self.request.data['board_id'])
        disease=Disease.objects.get(name=self.request.data['disease_name'])
        serializer.save(board=board,disease=disease)
        
    #삭제처리 안됨
    #[delete] /plants_by_detail/{id}
    def perform_destroy(self, instance):
        #instance.is_delete = '1'
        instance.save()



