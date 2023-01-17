import datetime, os

from board.models import Board
from member.models import Member

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
#from .serializers import BoardSerializer
from rest_framework import status,views
from rest_framework.decorators import action

class Predict(views.APIView):
    def post(self,request):
        return Response("predict called")


class Train(views.APIView):
    def post(self,request):
        return Response("train called")