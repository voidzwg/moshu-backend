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
            prototype = Prototype.objects.get(id=picid)
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
            prototype = Prototype.objects.get(id=picid)
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
        width = request.POST.get('width')
        height = request.POST.get('height')
        prototype = Prototype(pid=pid, name=name, data='', width=width, height=height)
        prototype.save()
        return JsonResponse({'errno': 0, 'msg': "创建成功", 'picid': prototype.id})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def delete(request):
    if request.method == 'POST':
        picid = request.POST.get('picid')
        try:
            prototype = Prototype.objects.get(id=picid)
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
            prototype = Prototype.objects.get(id=picid)
        except:
            return JsonResponse({'errno': 2, 'msg': "原型设计不存在"})
        return prototype_serialize([prototype])
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def search_design(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        keyword = request.POST.get('keyword')
        if keyword == '':
            return JsonResponse({'errno': 5, 'msg': "搜索内容不能为空！"})
        prototypes = Prototype.objects.filter(pid=pid)
        name_list = []
        for prototype in prototypes:
            name_list.append(prototype.name)
        choices_list = [name_list]
        list_results = fuzzy_search(keyword, choices_list)
        results = []
        for key in list_results:
            filters = prototypes.filter(name=key[0])
            if filters:
                for item in filters:
                    results.append(item)
                continue
        unique_results = list(set(results))
        unique_results.sort(key=results.index)
        return prototype_serialize(unique_results)
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


