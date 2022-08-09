import os
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
        data = request.FILES.get('data')
        try:
            prototype = Prototype.objects.get(id=picid)
        except:
            return JsonResponse({'errno': 2, 'msg': "原型设计不存在"})
        prototype.data = data.name
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
        pid = request.POST.get('pid')
        uid = request.POST.get('uid')
        name = request.POST.get('name')
        width = request.POST.get('width')
        height = request.POST.get('height')
        model_name = request.POST.get('model_name')
        if name == '':
            return JsonResponse({'errno': 2, 'msg': "名字不能为空"})
        try:
            project = Projects.objects.get(id=pid)
        except:
            return JsonResponse({'errno': 2, 'msg': "项目不存在"})
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 2, 'msg': "用户不存在"})
        now_time = datetime.datetime.now()
        file_name = now_time.strftime('%Y%m%d%H%M%S%f_') + str(pid) + '_' + model_name
        content = ''
        print("prepare to open file")
        with open(os.path.join(settings.MEDIA_ROOT, 'documents', model_name), 'rt') as model_file:
            while True:
                msg = model_file.read(READ_LENGTH)
                if msg == '':
                    break
                content += msg
        print("Already open model file", content[:80])
        with open(os.path.join(settings.MEDIA_ROOT, 'documents', file_name), 'at') as new_file:
            while content:
                msg = content[:READ_LENGTH]
                new_file.write(msg)
                content = content[READ_LENGTH:]
        print("Aready open the goal file", file_name)
        prototype = Prototype(pid=project, uid=user, name=name, data=file_name, width=width, 
                              height=height, create_time=now_time, modify_time=now_time)
        prototype.save()
        print("Already saved in database", now_time)
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
        data = []
        for prototype in prototype_list:
            try:
                user = Users.objects.get(id=prototype.uid.id)
                name = user.name
                username = user.username
            except Exception as e:
                print(e)
                name = None
                username = None
            json = {
                'picid': prototype.id,
                'name': prototype.name,
                'create_time': prototype.create_time,
                'modify_time': prototype.modify_time,
                'creator_username': username,
                'creator_name': name,
            }
            data.append(json)
        return JsonResponse(data, safe=False)
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


def get_templates(request):
    if request.method == 'GET':
        templates = Template.objects.all()
        if templates.count() == 0:
            return JsonResponse({'errno': 0, 'msg': "无模板"})
        data = []
        for t in templates:
            tmp = {
                'id':t.id,
                'name':t.name,
            }
            data.append(tmp)
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


def open_template(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id is None:
            JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            t = Template.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "模板不存在"})
        data = {
            'data':t.data,
            'width':t.width,
            'height':t.height,
        }
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})