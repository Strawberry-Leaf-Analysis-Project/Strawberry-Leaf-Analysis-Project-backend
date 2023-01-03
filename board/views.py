import datetime

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from board.models import Board
from member.models import Member
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import random, os

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

    rsBoard=Board.objects.all()

    return render(request,"boardForm.html",{
        'context':context,'rsBoard':rsBoard})

def board_write(request):
    context={}

    context['key'] = request.session['key']
    context['name'] = request.session['name']

    return render(request,"boardWriteForm.html",context)

#@csrf_exempt
def board_newWrite(request):
    atitle = request.POST['title']
    aexplain = request.POST['explain']
    userkey = request.POST['key']

    user=Member.objects.get(key=userkey)
    name_date = str(datetime.datetime.today().year) + '_' + str(datetime.datetime.today().month) + '_' + str(
        datetime.datetime.today().day)

    uploaded_file = request.FILES['ufile']
    name_old = uploaded_file.name
    name_ext = os.path.splitext(name_old)[1]
    name_new = 'O' + name_date + '_' + str(random.randint(1000000000, 9999999999))

    fs = FileSystemStorage(location='media/image/'+user.id)

    name = fs.save(name_new + name_ext, uploaded_file)

    rows = Board.objects.create(title=atitle, explain=aexplain, image=name,user_key=userkey,
                                views='0',like='0',date=datetime.datetime.now())

    return redirect('/board')

def board_detail(request,key):

    #이미지 삽입도 나중에 확인해봐야함
    rs = Board.objects.get(key=key)
    user= Member.objects.get(key=rs.user_key)
    rs.views=rs.views+1
    rs.save()

    return render(request,"boardDetail.html",{'data':rs,'user':user})