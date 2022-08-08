import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from com.funcs import *
from .models import *


# Author: zwg
# Create your views here.
@csrf_exempt
def get_info(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 2, 'msg': "用户不存在"})
        return user_serialize(user)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def update_info(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        profile = request.POST.get('profile')
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 2, 'msg': "用户不存在"})
        try:
            test_user = Users.objects.get(username=username)
        except:
            user.username = username
            user.name = name
            user.email = email
            user.profile = profile
            user.save()
            return JsonResponse({'errno': 0, 'msg': "修改成功！"})
        if user.username == username:
            user.name = name
            user.email = email
            user.profile = profile
            user.save()
            return JsonResponse({'errno': 0, 'msg': "修改成功！"})
        return JsonResponse({'errno': 2, 'msg': "用户名已被占用"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def update_password(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 2, 'msg': "用户不存在"})
        password = request.POST.get('password')
        if password != user.field_password:
            return JsonResponse({'errno': 3, 'msg': "密码错误"})
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if not check_password(password_1):
            return JsonResponse({'errno': 4, 'msg': "密码格式错误"})
        if password_2 != password_1:
            return JsonResponse({'errno': 4, 'msg': "密码不一致"})
        user.field_password = password_1
        user.save()
        return JsonResponse({'errno': 0, 'msg': "修改成功！"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_group(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 2, 'msg': "用户不存在"})
        members = Members.objects.filter(uid=user)
        data = []
        for member in members:
            json = {
                'name': member.gid.name
            }
            data.append(json)
        return JsonResponse(data, safe=False)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def set_avatar(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        avatar = request.FILES.get('avatar')
        if uid == '' or avatar == '':
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        # print(uid, avatar.name)
        if not avatar.name.lower().endswith(IMAGE_TAIL):
            print(avatar)
            return JsonResponse({'errno': 1002, 'msg': "文件格式错误"})
        pass
        try:
            user = Users.objects.get(id=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "用户不存在"})
        avatar_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + avatar.name
        try:
            user.avatar = avatar_name
            user.save()
        except Exception as e:
            return JsonResponse({'errno': 1004, 'msg': "未知错误"})
        f = open(os.path.join(settings.MEDIA_ROOT, 'avatars', avatar_name), 'wb')
        for i in avatar.chunks():
            f.write(i)
        f.close()
        return JsonResponse({'errno': 0, 'msg': "上传成功"})
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
