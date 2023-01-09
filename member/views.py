import os

from django.views.decorators.csrf import csrf_exempt
from member.models import Member

from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import MemberSerializer
from rest_framework.decorators import action
# Create your views here.

class MemberListAPI(viewsets.ModelViewSet):
    queryset=Member.objects.all()
    serializer_class = MemberSerializer

    existQueryset = Member.objects.filter(is_delete='0')

    #생성시 삭제된 id까지 고려할지 의문
    def create(self, request):
        serializer=self.get_serializer(data=request.data) #요청값->serializer
        exist=self.queryset.filter(id=request.data['id']) #id 중복 검사

        if len(exist) !=0:
            return Response({"message":"same id user exist "})
        if serializer.is_valid(): #입력값이 serializer에서 설정한 유효성 검사를 통과했다면
            serializer.save() #저장,is_valid 호출후 사용가능
            os.mkdir("media/image/" + str(request.data['id']))
            return Response(serializer.data) #해당값을 반환해줌 보내줌
        return Response(serializer.error) #is_valid 호출후에 사용가능

    def perform_destroy(self, instance):
        instance.is_delete='1'
        instance.save()

    #삭제처리하지 않은 유저들의 리스트
    # member/consist_userList
    @action(detail=False, methods=['GET']) #애매하네..
    def consist_userList(self, request):
        serializer = self.get_serializer(self.existQueryset, many=True)  # 요청값->serializer
        return Response(serializer.data)

    # member/{key}/change_password/?password={}&apaasword={}
    @action(detail=True,methods=['PATCH'])
    def change_password(self,request,pk=None):
        user=self.existQueryset.filter(key=pk)
        pwd=request.data['password']
        apwd = request.data['apassword']

        if pwd=='' or apwd=='':
            return Response("빈칸을 채워주세요")
        if pwd!=apwd:
            return Response("입력한 두 비밀번호가 일치하지 않습니다.")

        for u in user:
            u.password=pwd
            u.save()

        serializer=self.get_serializer(user,many=True)
        return Response(serializer.data)

    #member/{key}/change_name/?name={}
    @action(detail=True, methods=['PATCH'])
    def change_name(self, request, pk=None):
        user = self.existQueryset.filter(key=pk)
        name = request.data['name']

        if name == '' :
            return Response({"message":"빈칸을 채워주세요"})

        for u in user:
            u.name = name
            u.save()

        serializer = self.get_serializer(user, many=True)
        return Response(serializer.data)

    # member/login/?id={}&password={}
    @csrf_exempt
    @action(detail=False,methods=['POST'])
    def login(self,request):
        if 'key' in request.session:
            return Response({"message":"이미 로그인 되어 있는 회원입니다."})

        id=request.data['id']
        pwd=request.data['password']

        if id=='' or pwd=='':
            return Response({"message":"빈칸을 채워주세요"})

        user = self.existQueryset.filter(id=id)

        if len(user) != 0 :
            for u in user:
                if u.password==pwd:
                    request.session['key'] = u.key
                    request.session['id'] = u.id
                    request.session['name'] = u.name

                    return Response({"message": "로그인 성공",
                                     "key":u.key,
                                     'id':request.session['id']})
        return Response({"message":"아이디나 비밀번호가 잘못되었습니다."})

    # member/logout
    @csrf_exempt
    @action(detail=False,methods=['POST'])
    def logout(self,request):
        request.session.flush()
        return Response({"message":"정상적으로 로그아웃되었습니다."})
