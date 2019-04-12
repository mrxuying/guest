from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import time

# Create your views here.
def index(request):
    return render(request,'index.html')


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if username == 'admin' and password == 'admin123':
            response = HttpResponseRedirect('/event_manage/')
            response.set_cookie('user',username,3600)   #添加浏览器cookie,3600是cookie存在的时间，单位是秒
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})

def event_manage(request):
    username = request.COOKIES.get('user','')       #读取浏览器cookie
    return render(request,"event_manage.html",{"user":username})
