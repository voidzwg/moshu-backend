from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from com.funcs import *
from .models import *


# Author: zwg
# Create your views here.
@csrf_exempt
def store(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        data = request.POST.get('data')
        name = request.POST.get('name')
        prototype = Prototype(pid=pid, data=data, name=name)
        prototype.save()
        return JsonResponse({'errno': 0, 'msg': "创建成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_design(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        prototype_list = Prototype.objects.filter(pid=pid)
        data = []
        for prototype in prototype_list:
            json = {
                'picid': prototype.id,
                'data': prototype.data,
                'name': prototype.name
            }
            data.append(json)
        return JsonResponse(data, safe=False)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})

