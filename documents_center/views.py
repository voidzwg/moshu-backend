from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def documents_center(request):
    if request.method == 'GET':
        gid = request.GET.get('gid')
        if gid is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})