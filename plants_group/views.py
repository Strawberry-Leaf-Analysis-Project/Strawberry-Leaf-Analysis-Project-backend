import os

from member.models import Member
from plants_group.models import PlantsGroup

from rest_framework.response import Response
from .serializers import PlantsGroupSerializer
from rest_framework import viewsets,status
from rest_framework.decorators import action

class PlantsGroupListAPI(viewsets.ModelViewSet):
    queryset = PlantsGroup.objects.all()
    serializer_class = PlantsGroupSerializer

    #[post] /plants_group
    def perform_create(self,serializer):
        user=Member.objects.get(id=self.request.session['id'])
        os.mkdir("media/image/" + user.id + "/" + self.request.data['name'])
        serializer.save(user=user) 

    #삭제 수행안됨
    #[delete] plants_group/{id}/
    def perform_destroy(self, instance):
        #instance.is_delete = '1'
        instance.save()

    # [patch] plants_group/{id}/change_board/
    # 유저 비번 바꾸는거랑 동일한 방식으로 보내면 됨
    @action(detail=True,methods=['PATCH'])
    def change_status(self,request,pk=None):
        plants=self.queryset.get(id=pk)
        status=request.data['status']

        if status=='1':
            plants.status='1'
        else:
            plants.status='0'

        plants.save()

        serializer=self.get_serializer(plants)
        return Response(serializer.data)

    # 위와 동일/ 필요값 name:변경할 이름
    # [patch] plants_group/{id}/change_name/
    @action(detail=True, methods=['PATCH'])
    def change_name(self, request, pk=None):
        name = request.data['name']
        user = Member.objects.get(id=self.request.session['id'])
        exist=self.queryset.filter(user=user,name=name)

        if len(exist) !=0:
            return Response({"message":"동일한 이름의 작물이 있습니다. 다른 이름을 등록해주세요"})

        plants = self.queryset.get(id=pk)

        os.rename("media/image/" + user.id + "/" + plants.name,"media/image/" + user.id + "/" + name)

        plants.name=name
        plants.save()

        serializer = self.get_serializer(plants)
        return Response(serializer.data)


