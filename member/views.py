import json
import os

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from member.models import Member
# Create your views here.
def member_register(request):
    return render(request,"createMembersForm.html")

@csrf_exempt
def member_idcheck(request):
    context={}
    memid = request.GET['id']

    rs=Member.objects.filter(id=memid)
    if(len(rs)) > 0:
        context['flag']='1'
        context['result_msg']='사용자 아이디 중복'
    else:
        context['flag'] = '0'
        context['result_msg'] = '사용가능한 아이디'

    return JsonResponse(context,content_type="application/json")

@csrf_exempt
def member_insert(request):
    context={}

    memid = request.GET['id']
    mempwd = request.GET['password']
    memname = request.GET['name']

    rs=Member.objects.create(id=memid,password=mempwd,name=memname,
                            visited='0',is_staff='0')

    os.mkdir("media/image/"+memid)
    context['result_msg'] = '회원가입되었습니다. Home에서 로그인해주세요'

    return JsonResponse(context, content_type="application/json")

def login(request):
    return render(request,"login.html")

@csrf_exempt
def member_login(request):
    context={}

    memid = request.GET['id']
    mempwd = request.GET['password']

    if 'key' in request.session:
        context['flag'] = '1'
        context['result_msg'] = '이미 로그인 되어있습니다.'
    else:
        rs=Member.objects.filter(id=memid,password=mempwd)

        if(len(rs))==0:
            context['flag'] = '1'
            context['result_msg'] = '아이디 혹은 비밀번호가 다릅니다.'
        else:
            rsMember=Member.objects.get(id=memid,password=mempwd)
            memkey=rsMember.key
            memname=rsMember.name
            rsMember.visited='1'
            rsMember.save()

            request.session['key']=memkey
            request.session['name'] = memname

            context['flag'] = '0'
            context['result_msg'] = '로그인 되었습니다.'

    return JsonResponse(context, content_type="application/json")

@csrf_exempt
def member_logout(request):
    context={}

    request.session.flush()

    return redirect('/')

@csrf_exempt
def member_statchange(request):
    context = {}

    context['key'] = request.session['key']
    context['name'] = request.session['name']

    return render(request, "changeMemberStat.html", context)

@csrf_exempt
def member_changeName(request):
    context = {}

    memkey = request.GET['key']
    memname = request.GET['name']

    rs = Member.objects.filter(name=memname)

    if (len(rs)) !=0:
        context['flag'] = '1'
        context['result_msg'] ='중복된 닉네임입니다.'
    else:
        rsMember = Member.objects.get(key=memkey)
        rsMember.name=memname
        rsMember.save()

        request.session['key'] = memkey
        request.session['name'] = memname

        context['flag'] = '0'
        context['result_msg'] = '닉네임이 변경되었습니다.'

    return JsonResponse(context, content_type="application/json")

@csrf_exempt
def member_changePassword(request):
    context = {}

    memkey = request.GET['key']
    mempassword = request.GET['password']


    rsMember = Member.objects.get(key=memkey)
    rsMember.password=mempassword
    rsMember.save()

    request.session.flush()

    context['result_msg'] = '비밀번호가 변경되었습니다. 다시 로그인해주세요.'

    return JsonResponse(context, content_type="application/json")
