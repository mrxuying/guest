from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import time
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'index.html')


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username = username ,password = password)
        if user is not None:
            auth.login(request,user)#登录
            response = HttpResponseRedirect('/event_manage/')
            #response.set_cookie('user',username,3600)   #添加浏览器cookie,3600是有效时间，单位s"user"是cookie的名称；
            request.session['user'] = username  #将session信息添加到浏览器
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})

@login_required
def event_manage(request):
    #username = request.COOKIES.get('user','')       #读取浏览器cookie
    username = request.session.get('user','')   #读取浏览器session
    return render(request,"event_manage.html",{"user":username})
