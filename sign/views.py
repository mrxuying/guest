from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import time
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import get_object_or_404
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
    event_list = Event.objects.all()
    username = request.session.get('user','')   #读取浏览器session
    return render(request,"event_manage.html",{"user":username,"events":event_list})

@login_required
def guest_manage(request):
    username = request.session.get('user','')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,2) ##将所有嘉宾传给Paginator,每两条为一页
    page = request.GET.get('page')      ##通过GET请求来返回页数
    try:
        ##尝试请求第page页
        contacts = paginator.page(page)
    except PageNotAnInteger:
        ##如果抛出page不是整数 的异常，则返回第一页的数据
        contacts = paginator.page(1)
    except Emptypage:
        ##如果返回的是空页面异常，则返回最后一页的数据
        contacts = paginator.page(paginator.num_pages)
    ##返回contacts页面数据
    return render(request,"guest_manage.html",{"user":username,"guests":contacts})

@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get("name","")
    event_list = Event.objects.filter(name_contains=search_name)
    return render(request,"event_manage.html",{"user":username,"events":event_list})

#签到页面
@login_required
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)
    return render(request, 'sign_index.html', {'event':event})

@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event,id=eid)
    phone = request.POST.get('phone','')
    print(phone)

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html',{'event':event,'hint':'phone_error.'})

    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html',{'event':event,'hint':'event_id or phone error.'})

    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html',{'event':event,'hint':'user has sign in.'})

    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html',{'event':event,'hint':'sign in success.','guest':result})


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response
