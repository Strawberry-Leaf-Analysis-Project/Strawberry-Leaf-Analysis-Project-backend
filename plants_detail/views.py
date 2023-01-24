import datetime, os

from board.models import Board
from plants_detail.models import PlantsDetail

from plants_group.models import PlantsGroup
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
from .serializers import PlantsDetailSerializer
from rest_framework import viewsets,status
from rest_framework.decorators import action

class PlantsDetailListAPI(viewsets.ModelViewSet):
    queryset = PlantsDetail.objects.all()
    serializer_class = PlantsDetailSerializer

    #필요값: id:게시판 id
    #[post] /plants_detail
    def perform_create(self, serializer):
        board=Board.objects.get(id=self.request.data['id'])
        serializer.save(board=board)

    #삭제 처리안됨
    #[delete] /plants_detail/{id}
    def perform_destroy(self, instance):
        #instance.is_delete = '1'
        instance.save()




