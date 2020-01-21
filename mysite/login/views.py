from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from . import models
import hashlib

# Create your views here.
def home(request):
    if request.session.get('is_login',None):
        return render(request,'home_login.html')
    else:
        return render(request,'home_logout.html')

def hash_code(p,salt='xixi'):
    h = hashlib.sha256()
    p += salt
    h.update(p.encode('utf-8'))   #如果不加'utf-8',在输入密码时，用的又是中文输入法，会触发‘CSRF验证失败的错误’
    return h.hexdigest()


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
            
            if user.password == hash_code(password):
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
    if request.session.get('is_login',None):
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        same_name = models.User.objects.filter(name=username)
        same_email = models.User.objects.filter(email=email)

        if same_name:
            message = '用户名已被注册'
            return render(request, 'login/register.html', {'message': message})
        else:
            if password1 != password2:
                message = '两次输入的密码不同'
                return render(request,'login/register.html',{'message':message})

            if same_email:
                message = '邮箱已被注册'
                return render(request, 'login/register.html', {'message': message})
            
            new_user = models.User()
            new_user.name = username
            new_user.password = hash_code(password1)
            new_user.email = email
            new_user.save()
            print('注册成功')
            return HttpResponseRedirect(reverse('login:login'))
    return render(request,'login/register.html')

def logout(request):
    if not request.session.get('is_login',None):
        return HttpResponseRedirect(reverse('login:login'))
    request.session.flush()
    return HttpResponseRedirect(reverse('login:login'))
