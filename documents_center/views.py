from django.http import JsonResponse
from django.shortcuts import render
from com.funcs import *
# Create your views here.
from project_manage.views import open_document
def documents_center(request):
    if request.method == 'POST':
        gid = request.POST.get('gid')
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

def create_document(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        name = request.POST.get('name')
        model_name = request.POST.get('model_name')
        uid = request.POST.get('uid')
        if name == '':
            return JsonResponse({'errno': 2, 'msg': "名字不能为空"})
        try:
            project = Projects.objects.get(id=pid)
        except:
            return JsonResponse({'errno': 2, 'msg': "项目不存在"})
        try:
            user = Users.objects.get(id=uid)
        except:
            user = None
        now_time = datetime.datetime.now()
        file_name = now_time.strftime('%Y%m%d%H%M%S%f_') + str(pid) + '_' + model_name
        if copy_file(model_name, file_name):
            return JsonResponse({'errno': 6666, 'msg': "文件创建失败"})
        try:
            document = Document(pid=project,uid=user,data=file_name, name=name, create_time=now_time, modify_time=now_time)
            document.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 9999, 'msg': "数据库存储出错了"})
        print("Aready saved in database")
        return JsonResponse({'errno': 0, 'msg': "创建成功", 'docid': document.id})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})