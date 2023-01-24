import os

from argon2.exceptions import VerifyMismatchError
from django.views.decorators.csrf import csrf_exempt
from member.models import Member

from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import MemberSerializer
from rest_framework.decorators import action
from argon2 import PasswordHasher
# Create your views here.

class MemberListAPI(viewsets.ModelViewSet):
    queryset=Member.objects.all()
    serializer_class = MemberSerializer
    existQueryset = Member.objects.filter(is_delete='0')
    ph=PasswordHasher()


    #생성시 삭제된 id까지 고려할지 의문
    def create(self, request):
        exist=self.queryset.filter(id=request.data['id']) #id 중복 검사

        context={}
        if len(exist) !=0:
            return Response({"message":"same id user exist "})

        if request.data['email']=='':
            return Response({"message":"이메일이 안들어옴"})

        pwd_hash = self.ph.hash(request.data['password'])

        context['id'] = request.data['id']
        context['password'] = pwd_hash
        context['name'] = request.data['name']
        context['email']=request.data['email']

        serializer = self.get_serializer(data=context)  # 요청값->serializer

        if serializer.is_valid(): #입력값이 serializer에서 설정한 유효성 검사를 통과했다면
            serializer.save() #저장,is_valid 호출후 사용가능
            os.mkdir("media/image/" + str(request.data['id']))
            return Response(serializer.data) #해당값을 반환해줌 보내줌
        return Response(serializer.error) #is_valid 호출후에 사용가능

    def perform_destroy(self, instance):
        instance.is_delete='1'
        instance.save()

    #삭제처리하지 않은 유저들의 리스트(수정 필요 & 굳이 있어야할 필요가 있는지)
    # member/consist_userList
    @action(detail=False, methods=['GET']) #애매하네..
    def consist_userList(self, request):
        serializer = self.get_serializer(self.existQueryset, many=True)  # 요청값->serializer
        return Response(serializer.data)

    # member/{key}/change_password/?password={}&apaasword={}
    @action(detail=True,methods=['PATCH'])
    def change_password(self,request,pk=None):
        user=self.existQueryset.filter(id=pk)
        pwd=request.data['password']
        apwd = request.data['apassword']

        if pwd=='' or apwd=='':
            return Response("빈칸을 채워주세요")
        if pwd!=apwd:
            return Response("입력한 두 비밀번호가 일치하지 않습니다.")

        pwd_hash=self.ph.hash(pwd)
        for u in user:
            u.password = pwd_hash
            u.save()

        serializer=self.get_serializer(user,many=True)
        return Response(serializer.data)

    #member/{key}/change_name/?name={}
    @action(detail=True, methods=['PATCH'])
    def change_name(self, request, pk=None):
        user = self.existQueryset.filter(id=pk)
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
        if 'id' in request.session:
            return Response({"message":"이미 로그인 되어 있는 회원입니다."})

        id=request.data['id']
        pwd=request.data['password']

        if id=='' or pwd=='':
            return Response({"message":"빈칸을 채워주세요"})

        try:
            user = self.existQueryset.get(id=id)

            self.ph.verify(user.password,pwd)

            request.session['id'] = user.id
            request.session['name'] = user.name

            return Response({"message": "로그인 성공",
                             'id': user.id,
                             'name':user.name,
                             })

        except Member.DoesNotExist:
            return Response({"message": "아이디나 비밀번호가 잘못되었습니다."})

        except VerifyMismatchError:
            return Response({"message": "아이디나 비밀번호가 잘못되었습니다."})

    # member/logout
    @csrf_exempt
    @action(detail=False,methods=['POST'])
    def logout(self,request):
        response = Response({"message":"정상적으로 로그아웃되었습니다."})
        response.delete_cookie('hit')
        request.session.flush()
        return response

    #[post] member/password_check 회원가입시 or 비밀번호 변경시 비밀번호 2번 입력하고 확인하는 과정을 따로 기능으로 만듬
    @action(detail=False,methods=['POST'])
    def password_check(self,request):
        pwd=request.data['password']
        check_pwd=request.data['check_password']

        if pwd=="" or check_pwd=="":
            return Response({"flag": 0,
                             "message": "빈칸을 채워주세요."})
        if pwd!=check_pwd:
            return Response({"flag": 0,
                             "message": "두 비밀번호가 일치하지 않습니다."})
        return Response({"flag": 1,
                             "message": "비밀번호가 일치합니다."})
