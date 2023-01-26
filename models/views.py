import datetime, os
import cv2
import matplotlib.pyplot as plt

from django.core.files.base import ContentFile
from PIL import Image

from board.models import Board
from member.models import Member
from temp_image.models import TempImage

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
from temp_image.serializers import TempImageSerializer
from rest_framework import status,views
from rest_framework.decorators import action

class Predict(views.APIView):
    def post(self,request):
        context={}
        image = cv2.imread("C:\Strawberry-Leaf-Analysis-Project-backend\media\image\shin5773\\temp_image.jpg")
        c_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        user=Member.objects.get(id=request.data['id'])

        ret,buf=cv2.imencode('.jpg',c_image)
        content=ContentFile(buf.tobytes())

        t=TempImage()
        t.user=user
        t.image.save('output.jpg',content)
        return Response()


class Train(views.APIView):
    def post(self,request):
        return Response("train called")