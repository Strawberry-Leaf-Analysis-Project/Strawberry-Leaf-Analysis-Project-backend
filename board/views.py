import datetime

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from board.models import Board
from member.models import Member
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import random, os

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BoardSerializer
from rest_framework import viewsets
from rest_framework.decorators import action

class BoardListAPI(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    existQueryset = Board.objects.filter(is_delete='0')

    #[post] /board
    def perform_create(self, serializer):
        user=Member.objects.get(id=self.request.session['id'])
        serializer.save(user=user)
    '''
    def create(self, request):
        user=Member.objects.get(key=request.session['key'])
        request.data['user']=user
        serializer=self.get_serializer(data=request.data) #요청값->serializer

        if serializer.is_valid(): #입력값이 serializer에서 설정한 유효성 검사를 통과했다면
            serializer.save() #저장,is_valid 호출후 사용가능
            return Response(serializer.data) #해당값을 반환해줌 보내줌
        return Response(serializer.error) #is_valid 호출후에 사용가능
    '''

    #[delete] board/{key}
    def perform_destroy(self, instance):
        instance.is_delete = '1'
        instance.save()

    #해당 유저가 작성한 게시판 목록 반환
    #[get] board/personal_board
    @action(detail=False,methods=['GET'])
    def personal_board(self,request):
        user = Member.objects.get(id=self.request.session['id'])
        user_board=self.existQueryset.filter(user=user)

        serializer=self.get_serializer(user_board,many=True)
        return Response(serializer.data)
'''
# Create your views here.
def home(request):
    context={}

    if request.session.has_key('key'):
        key=request.session['key']
        name=request.session['name']
    else:
        key=None
        name=None

    context['key']=key
    context['name']=name

    return render(request,"home.html",context)

def board_home(request):
    context={}

    context['key'] = request.session['key']
    context['name'] = request.session['name']

    rsBoard=Board.objects.filter(is_delete='0')
    rsLatest = Board.objects.filter(is_delete='0').order_by('-date')
    rsLikes = Board.objects.filter(is_delete='0').order_by('-like')
    rsViews = Board.objects.filter(is_delete='0').order_by('-views')

    return render(request,"boardForm.html",{
        'context':context,'rsBoard':rsBoard,'latestBoard':rsLatest,'likesBoard':rsLikes,'viewsBoard':rsViews})

def board_write(request):
    context={}

    context['key'] = request.session['key']
    context['name'] = request.session['name']
    context['flag'] = request.GET['flag']

    return render(request,"boardWriteForm.html",context)

#@csrf_exempt
def board_newWrite(request):
    atitle = request.POST['title']
    aexplain = request.POST['explain']
    userkey = request.POST['key']
    uploaded_file = request.FILES['ufile']
    flag=request.POST['flag']

  

    
    이름 변경 및 저장(static 방식)
    user=Member.objects.get(key=userkey)
    name_date = str(datetime.datetime.today().year) + '_' + str(datetime.datetime.today().month) + '_' + str(
        datetime.datetime.today().day)

    uploaded_file = request.FILES['ufile']
    name_old = uploaded_file.name
    name_ext = os.path.splitext(name_old)[1]
    name_new = 'O' + name_date + '_' + str(random.randint(1000000000, 9999999999))

    fs = FileSystemStorage(location='media/image/'+user.id)

    name = fs.save(name_new + name_ext, uploaded_file)
   

    
    rows = Board.objects.create(title=atitle, explain=aexplain, image=uploaded_file,user_key=userkey,
                                views='0',like='0',date=datetime.datetime.now(),is_delete='0')

    if flag == '0':
        return redirect('/board')
    else:
        return redirect('/personal_board')

def board_detail(request,key,flag):

    #이미지 삽입도 나중에 확인해봐야함
    rs = Board.objects.get(key=key)
    user= Member.objects.get(key=rs.user_key)
    rs.views=rs.views+1
    rs.save()
    context={}
    context['key']=request.session['key']
    context['flag']=flag
    return render(request,"boardDetail.html",{'data':rs,'user':user,'context':context})

def board_delete(request,key,flag):
    rsQuery = Board.objects.filter(key=key)
    rsQuery.update(is_delete=1)

    if flag == 0:
        return redirect('/board')
    else:
        return redirect('/personal_board')
def personalBoard_home(request):
    context={}

    user_key=request.session['key']
    context['key'] = user_key
    context['name'] = request.session['name']

    rsBoard=Board.objects.filter(is_delete='0',user_key=user_key)


    return render(request,"personalBoardForm.html",{
        'context':context,'rsBoard':rsBoard})
'''