import os

from member.models import Member
from temp_image.models import TempImage
from static import test

from rest_framework.response import Response
from .serializers import TempImageSerializer
from rest_framework import viewsets,status
from rest_framework.decorators import action

class TempImageListAPI(viewsets.ModelViewSet):
    queryset = TempImage.objects.all()
    serializer_class = TempImageSerializer

    #[post] /plants_group
    def perform_create(self,serializer):
        user=Member.objects.get(id=self.request.data['id'])
        serializer.save(user=user)
        # test.testprint() / segmentation 이미지 리터


    #삭제 수행안됨
    #[delete] plants_group/{id}/
    def perform_destroy(self, instance):
        #instance.is_delete = '1'
        instance.save()
