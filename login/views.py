from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from com.funcs import *
from .models import *

user = Users.objects.all()
print(user)
# Author: zwg
# Create your views here.
@csrf_exempt  # 跨域设置
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or password is None:
            return JsonResponse({'errno': 1, 'msg': "请输入用户名和密码"})
        pass
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})

