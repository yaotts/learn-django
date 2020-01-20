from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from . import models

# Create your views here.
def home(request):
    if request.session.get('is_login',None):
        return render(request,'home_login.html')
    else:
        return render(request,'home_logout.html')

def login(request):
    if request.session.get('is_login',None):
        return HttpResponseRedirect(reverse('home'))
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username and password:
        if username.strip() == username:
            try:
                user = models.User.objects.get(name__exact=username)  #windows下的mysql查询是不区分大小写的
            except:
                message = '用户名不存在！'
                return render(request, 'login/login.html',{'message': message})
            
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session.set_expiry(0)
                return HttpResponseRedirect(reverse('home'))
            else:
                message = '密码错误!'
                return render(request, 'login/login.html',{'message': message})
        else:
            message = '用户名不能以空格开头或结束！'
            return render(request, 'login/login.html',{'message': message})
    else:
        return render(request,'login/login.html')


def register(request):
    pass
    return render(request,'login/register.html')

def logout(request):
    if not request.session.get('is_login',None):
        return HttpResponseRedirect(reverse('login:login'))
    request.session.flush()
    return HttpResponseRedirect(reverse('login:login'))
