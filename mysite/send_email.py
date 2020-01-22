import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':

    subject = '网站注册验证——Yaolp的个人网站'
    from_email = '835548994@qq.com'
    to = ['yaotts@hotmail.com']
    text_content = '您正在使用此邮箱注册我们网站的账号，这是一封验证邮件，请点此完成验证。'
    html_content = '<p>您好，</p><p>您正在使用此邮箱注册我们网站的账号，这是一封验证邮件，<a href="www.baidu.com" target=blank>点此</a>完成注册。</p>'
    msg=EmailMultiAlternatives(subject=subject,body=text_content,from_email=from_email,to=to)
    msg.attach_alternative(html_content,"text/html")
    msg.send()

    
