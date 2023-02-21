from board.models import Board
from disease.models import Disease
from plants_by_disease.models import PlantsByDisease

from member.models import Member
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
from .serializers import BoardLikeByUser
from rest_framework import viewsets,status
from rest_framework.decorators import action

class BoardLikeByUserListAPI(viewsets.ModelViewSet):
    queryset = BoardLikeByUser.objects.all()
    serializer_class = BoardLikeByUser

    existQueryset=BoardLikeByUser.objects.filter(is_delete='0')

    #필요값:board_id:게시판의 id,disease_name:질병명
    #[post] /board_like_by_user/
    def perform_create(self, serializer):
        board=Board.objects.get(id=self.request.data['board_id'])
        user=Member.objects.get(name=self.request.data['id'])
        serializer.save(board=board,member=user)

    #[delete] /board_like_by_user/{id}
    def perform_destroy(self, instance):
        instance.is_delete = '1'
        instance.save()




