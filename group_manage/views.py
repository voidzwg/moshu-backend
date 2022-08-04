from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from com.funcs import *
from .models import *


# Author: zwg
# Create your views here.
@csrf_exempt
def create_group(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        name = request.POST.get('name')
        if name is None:
            return JsonResponse({'errno': 2, 'msg': "名字不能为空"})
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 3, 'msg': "用户不存在"})
        new_groups = Groups(name=name, unum=1, pnum=0)
        new_groups.save()
        new_members = Members(gid=new_groups, uid=user, field_role=2)
        new_members.save()
        return JsonResponse({'errno': 0, 'msg': "创建成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_created_group(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 3, 'msg': "用户不存在"})
        members = Members.objects.filter(uid=user, field_role=2)
        group_list = []
        for member in members:
            group_list.append(member.gid)
        return group_serialize(group_list)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_managed_group(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 3, 'msg': "用户不存在"})
        members = Members.objects.filter(uid=user, field_role=1)
        group_list = []
        for member in members:
            group_list.append(member.gid)
        return group_serialize(group_list)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_participated_group(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 3, 'msg': "用户不存在"})
        members = Members.objects.filter(uid=user, field_role=0)
        group_list = []
        for member in members:
            group_list.append(member.gid)
        return group_serialize(group_list)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def dismiss(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        if uid is None or gid is None:
            return JsonResponse({'errno': 1002, 'msg': "uid或gid为空，请检查参数名是否为\'gid\',\'uid\'"})
        try:
            member = Members.objects.get(gid=gid, uid=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在或未知错误"})
        if member.field_role != 2:
            return JsonResponse({'errno': 1004, 'msg': "不是创建者，不能解散团队！"})
        else:
            try:
                group = Groups.objects.get(id=gid)
            except Exception as e:
                print(e)
                return JsonResponse({'errno': 1003, 'msg': "不存在或未知错误"})
            else:
                group.delete()
                return JsonResponse({'errno': 0, 'msg': "解散成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
