from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from com.funcs import *
from .models import *


# Author: zwg
# Create your views here.
@csrf_exempt  # 跨域设置
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or password is None:
            return JsonResponse({'errno': 2, 'msg': "请输入用户名和密码"})
        try:
            user = Users.objects.get(username=username)
        except:
            return JsonResponse({'errno': 2, 'msg': "用户不存在"})
        if password == user.field_password:
            return JsonResponse({'errno': 0, 'msg': "登录成功", 'uid': user.id})
        return JsonResponse({'errno': 2, 'msg': "密码不正确"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if username is None or password_1 is None:
            return JsonResponse({'errno': 2, 'msg': "请输入用户名和密码"})
        try:
            test_user = Users.objects.get(username=username)
        except:
            if not check_password(password_1):
                return JsonResponse({'errno': 2, 'msg': "密码格式错误"})
            if password_2 is None:
                return JsonResponse({'errno': 2, 'msg': "请确认密码"})
            if password_2 != password_1:
                return JsonResponse({'errno': 2, 'msg': "两次输入的密码不一致"})
            email = request.POST.get('email')
            if email is None:
                return JsonResponse({'errno': 3, 'msg': "请输入邮箱"})
            if not check_email(email):
                return JsonResponse({'errno': 3, 'msg': "邮箱格式错误"})
            new_user = Users(username=username, field_password=password_1, avatar=DEFAULT_AVATAR, email=email, gnum=0)
            new_user.save()
            return JsonResponse({'errno': 0, 'msg': "注册成功！"})
        return JsonResponse({'errno': 2, 'msg': "用户名已被占用"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})

