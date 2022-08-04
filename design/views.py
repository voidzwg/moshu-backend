from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from com.funcs import *
from .models import *


# Author: zwg
# Create your views here.
@csrf_exempt
def store(request):
    if request.method == 'POST':
        picid = request.POST.get('picid')
        data = request.POST.get('data')
        try:
            prototype = request.POST.get(id=picid)
        except:
            return JsonResponse({'errno': 2, 'msg': "原型设计不存在"})
        prototype.data = data
        prototype.save()
        return JsonResponse({'errno': 0, 'msg': "修改成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def rename(request):
    if request.method == 'POST':
        picid = request.POST.get('picid')
        name = request.POST.get('name')
        try:
            prototype = request.POST.get(id=picid)
        except:
            return JsonResponse({'errno': 2, 'msg': "原型设计不存在"})
        prototype.name = name
        prototype.save()
        return JsonResponse({'errno': 0, 'msg': "修改成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def create(request):
    if request.method == 'POST':
        pid = request.POST.get('picid')
        name = request.POST.get('name')
        prototype = Prototype(pid=pid, name=name, data='')
        prototype.save()
        return JsonResponse({'errno': 0, 'msg': "创建成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def delete(request):
    if request.method == 'POST':
        picid = request.POST.get('picid')
        try:
            prototype = request.POST.get(id=picid)
        except:
            return JsonResponse({'errno': 2, 'msg': "原型设计不存在"})
        prototype.delete()
        return JsonResponse({'errno': 0, 'msg': "删除成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_design(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        prototype_list = Prototype.objects.filter(pid=pid)
        return prototype_serialize(prototype_list)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_one_design(request):
    if request.method == 'POST':
        picid = request.POST.get('picid')
        try:
            prototype = Prototype.objects.get(picid=picid)
        except:
            return JsonResponse({'errno': 2, 'msg': "原型设计不存在"})
        return prototype_serialize([prototype])
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})

