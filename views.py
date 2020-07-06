from turtle import color

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

# Create your views here.

# 1.登录
from app import models
from app.models import Person, Company


def login(request):
    status = False
    if request.POST:
        username = request.POST.get('username', None)
        passwd = request.POST.get('passwd', None)
    else:
        username = request.get_signed_cookie('username', None, salt='xyz')
        passwd = request.get_signed_cookie('passwd', None, salt='xyz')
        userType = request.get_signed_cookie('userType', None, salt='xyz')

    user_obj = models.Person.objects.filter(name=username, password=passwd).first()
    if not user_obj:
        user_obj = models.Company.objects.filter(name=username, password=passwd).first()
        if not user_obj:
            return render(request, 'login.html', {'msg': '账号或密码有误'})
        else:
            status = True
            resp = redirect("/app/index/")
            resp.set_signed_cookie('username', username, salt='xyz', max_age=5)
            resp.set_signed_cookie('userType', userType, salt='xyz', max_age=5)
            resp.set_signed_cookie('status', status, salt='xyz', max_age=5)
            return resp

    else:
        status = True
        resp = redirect("/app/index/")
        resp.set_signed_cookie('username', username, salt='xyz', max_age=5)
        resp.set_signed_cookie('status', status, salt='xyz', max_age=5)
        return resp


# 2注册
def register(request):
    if request.POST:
        userType = 'personal'
        telnumber = request.POST.get('telNum', None)
        username = request.POST.get("username", None)
        passwd = request.POST.get("password", None)
        passwd2 = request.POST.get("password2", None)
        if passwd != passwd2:
            return render(request, 'register.html')
        else:
            user_obj = models.Person.objects.filter(telNum=telnumber).first()
            if not user_obj:
                user_obj = models.Person.objects.filter(name=username).first()
                if not user_obj:
                    # 2.把前台获取的数据添加到数据库表中
                    try:
                        # 构造实体集
                        Person.objects.create(telNum=telnumber, name=username, password=passwd, type=userType)
                        # 3.跳转页面
                        # 把数据存入cookie
                        resp = redirect("/app/login/")
                        resp.set_signed_cookie('username', username, salt='xyz', max_age=5)
                        resp.set_signed_cookie('passwd', passwd, salt='xyz', max_age=5)
                        resp.set_signed_cookie('userType', userType, salt='xyz', max_age=5)
                        # 把数据存入到session中
                        request.session['username'] = username
                        request.session['passwd'] = passwd
                        request.session['userType'] = userType
                        return resp
                    except:
                        # 未添加成功
                        messages.success(request, '注册失败')
                        return render(request, 'register.html')
                else:
                    messages.success(request, '注册失败，该用户名已存在')
                    return render(request, 'register.html')
            else:
                messages.success(request, '注册失败，该手机号已存在')
                return render(request, 'register.html')
    else:
        return render(request, 'register.html')



def registerc(request):
    if request.POST:
        userType = 'company'
        telnumber = request.POST.get("telNum", None)
        username = request.POST.get("username", None)
        passwd = request.POST.get("password", None)
        passwd2 = request.POST.get("password2", None)
        province = request.POST.get("province", None)
        city = request.POST.get("city", None)
        addr = province + city
        if passwd != passwd2:
            return render(request, 'registerc.html')
        else:
            user_obj = models.Company.objects.filter(telNum=telnumber).first()
            if not user_obj:
                user_obj = models.Company.objects.filter(name=username).first()
                if not user_obj:
                    # 2.把前台获取的数据添加到数据库表中
                    try:
                        # 构造实体集
                        Company.objects.create(telNum=telnumber, name=username, password=passwd, type=userType,
                                               address=addr)
                        # 3.跳转页面
                        # 把数据存入cookie
                        resp = redirect("/app/login/")
                        resp.set_signed_cookie('username', username, salt='xyz', max_age=5)
                        resp.set_signed_cookie('passwd', passwd, salt='xyz', max_age=5)
                        resp.set_signed_cookie('userType', userType, salt='xyz', max_age=5)
                        # 把数据存入到session中
                        request.session['username'] = username
                        request.session['passwd'] = passwd
                        request.session['userType'] = userType
                        return resp
                    except:
                        # 未添加成功
                        messages.success(request, '注册失败')
                        return render(request, 'registerc.html')
                else:
                    messages.success(request, '注册失败，该用户名已存在')
                    return render(request, 'registerc.html')
            else:
                messages.success(request, '注册失败，该手机号已存在')
                return render(request, 'registerc.html')
    else:
        return render(request, 'registerc.html')



# 3.主页
def index(request):
    status = request.get_signed_cookie('status', None, salt='xyz')
    username = request.get_signed_cookie('username', None, salt='xyz')
    if status:
        messages.success(request, '登录成功，欢迎：{0}'.format(username))
    else:
        messages.success(request, '未登录，请先登录')
    return render(request, 'index.html')
