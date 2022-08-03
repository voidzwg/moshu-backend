from django.http import JsonResponse
from django.core import serializers
from .models import *

def get_member(request):
    if request.method == 'POST':
        gid = request.POST.get('gid')
        if gid is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空，请检查参数名是否为\'gid\'"})
        try:
            members = Members.objects.filter(gid=gid)
            users = []
            for i in members:
                users.append(i.uid)
            users = serializers.serialize('json',users)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "未知错误"})
        return JsonResponse(users,safe=False)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def appoint(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        if gid is None or uid is None:
            return JsonResponse({'errno': 1002, 'msg': "uid或gid为空，请检查参数名是否为\'gid\',\'uid\'"})
        try:
            member = Members.objects.get(gid=gid,uid=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该用户或未知错误"})
        if member.field_role == 1:
            return JsonResponse({'errno': 1004, 'msg': "该用户已经为管理员！"})
        try:
            member.field_role=1
            member.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1005, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "任命成功！"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def delete(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        if gid is None or uid is None:
            return JsonResponse({'errno': 1002, 'msg': "uid或gid为空，请检查参数名是否为\'gid\',\'uid\'"})
        try:
            member = Members.objects.get(gid=gid, uid=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该用户或未知错误"})
        if member.field_role == 2:
            return JsonResponse({'errno': 1004, 'msg': "该用户为创建者，不能删除！"})
        try:
            member.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1005, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "删除成功！"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def revoke(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        if gid is None or uid is None:
            return JsonResponse({'errno': 1002, 'msg': "uid或gid为空，请检查参数名是否为\'gid\',\'uid\'"})
        try:
            member = Members.objects.get(gid=gid, uid=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该用户或未知错误"})
        if member.field_role == 0:
            return JsonResponse({'errno': 1004, 'msg': "该用户不是管理员"})
        if member.field_role == 2:
            return JsonResponse({'errno': 1004, 'msg': "该用户是创建者，不能撤销"})
        try:
            member.field_role = 0
            member.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1005, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "撤销成功！"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
