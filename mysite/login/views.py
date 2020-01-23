from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from . import models
import hashlib
import datetime

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

def send_email(recipient,name):
    from django.core.mail import EmailMultiAlternatives
    subject = '网站注册验证——Yaolp的个人网站'
    sender = '835548994@qq.com'
    text_content = '如果您看到此信息，说明您的邮箱不支持HTML文档，请开启后重新注册。'
    html_content = '''
    <p>您好，</p>
    <p>这是一封注册确认邮件，您正在使用此邮箱注册‘Yaolp的个人网站’。</p>
    <p>请点击<a href="http://{}/accounts/confirm/?name={}" target=_blank>部署后的网站地址</a>来确认您的注册。</p>
    <p>此链接有效期为{}天。</p>'''.format('127.0.0.1:8000',name,settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject=subject,body=text_content,from_email=sender,to=[recipient])
    msg.attach_alternative(html_content,"text/html")
    msg.send()



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
            
            if not user.has_confirmed:
                message = '该用户还未通过注册邮件确认'
                return render(request, 'login/login.html', {'message': message})
            
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

            send_email(email,username)
            message = '注册成功！请在邮箱确认后登陆。'
            #可以在login.html中预留弹窗的位置，在跳转后弹出此message.
            return HttpResponseRedirect(reverse('login:login'))
    return render(request,'login/register.html')

def logout(request):
    if not request.session.get('is_login',None):
        return HttpResponseRedirect(reverse('login:login'))
    request.session.flush()
    return HttpResponseRedirect(reverse('login:login'))


def confirm(request):
    name = request.GET.get('name',None)
    print(name)
    try:
        user = models.User.objects.get(name=name)
    except:
        message = '无效的确认请求！'
        return render(request,'login/confirm.html',{'message':message})

    now = datetime.datetime.now()
    c_time = user.create_time
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        message = '邮件已过期，请重新注册！'
        user.delete()
        return render(request,'login/confirm.html',{'message':message})
    else:
        user.has_confirmed = True
        user.save()
        message = '确认成功，您现在可以去登陆了！'
        return render(request,'login/confirm.html',{'message':message})
    
