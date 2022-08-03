from django.core import serializers
from django.http import JsonResponse
from .models import *

def get_project(request):
    if request.method == 'GET':
        gid = request.GET.get('gid')
        if gid is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空，请检查参数名是否为\'gid\'"})
        try:
            projects = Projects.objects.filter(gid=gid)
            projects= serializers.serialize('json', projects)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "未知错误"})
        return JsonResponse(projects, safe=False)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


def create(request):
    if request.method == 'POST':
        gid = request.POST.get('gid')
        uid = request.POST.get('uid')
        name = request.POST.get('name')
        if gid is None or uid is None or name is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            gid = Groups.objects.get(id=gid)
            uid = Users.objects.get(id=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该用户或团队"})
        try:
            newProject = Projects(gid=gid, uid=uid, name=name, available=0, status=0)
            newProject.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "创建成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


def rename(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        if id is None or name is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            project = Projects.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该项目"})
        try:
            project.name = name
            project.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "重命名成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def to_bin(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            project = Projects.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该项目"})
        try:
            project.available=1
            project.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "已移至回收站"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            project = Projects.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该项目"})
        try:
            project.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "删除成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def close(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            project = Projects.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该项目"})
        try:
            project.status=1
            project.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "项目结束成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
