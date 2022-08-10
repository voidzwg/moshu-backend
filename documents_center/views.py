from django.http import JsonResponse
from django.shortcuts import render
from com.funcs import *
# Create your views here.
from project_manage.views import open_document
def documents_center(request):
    if request.method == 'GET':
        gid = request.GET.get('gid')
        if gid is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            root = Files.objects.get(name=gid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "找不到根目录！"})
        try:
            next_list = root.get_children()
            data = []
            for node in next_list:
                name = node.name.split('_')[1]
                if name == 'Project':
                    name = '项目文档区'
                elif name == 'Data':
                    name = '数据'
                elif name == 'Others':
                    name = '其他文件夹'
                tmp = {
                    'root_id':root.id,
                    'id':node.id,
                    'name':name,
                    'type':node.isfile,
                }
                data.append(tmp)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误！"})
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def open_file(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            file = Files.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "找不到该文件或目录！"})
        if file.isfile:
            return open_document(request)
        try:
            next_list = file.get_children()
            data = []
            for node in next_list:
                if file.name.split('_')[1] == 'Project':
                    name = node.name.split('_')[2*node.level-1]
                else:
                    name = node.name.split('_')[node.level]
                tmp = {
                    'id': node.id,
                    'name': name,
                    'type':node.isfile,
                }
                data.append(tmp)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误！"})
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def create_file(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name =request.POST.get('name')
        type = request.POST.get('type')
        if id is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            file = Files.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "找不到该目录！"})

        try:
            name = file.name + '_' + name
            newFile = Files(name=name,parent=file,isfile=type)
            newFile.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误！"})
        return JsonResponse({'errno': 0, 'msg': "新建成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})