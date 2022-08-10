from django.http import JsonResponse
from django.shortcuts import render
from com.funcs import *
# Create your views here.


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
                    'root_id': root.id,
                    'id': node.id,
                    'name': name,
                    'type': node.isfile,
                }
                data.append(tmp)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误！"})
        return JsonResponse(data, safe=False)
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
            return open_document(file.document.id)
        try:
            next_list = file.get_children()
            data = []
            for node in next_list:
                if file.name.split('_')[1] == 'Project':
                    name = node.name.split('_')[2 * node.level - 1]
                else:
                    name = node.name.split('_')[node.level]
                tmp = {
                    'id': node.id,
                    'name': name,
                    'type': node.isfile,
                }
                data.append(tmp)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误！"})
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


def create_file(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        type = request.POST.get('type')
        if id is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            file = Files.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "找不到该目录！"})
        if type == 1:
            model_name = request.POST.get('model_name')
            uid = request.POST.get('uid')
            create_document(name, model_name, uid)
        try:
            name = file.name + '_' + name
            newFile = Files(name=name, parent=file, isfile=type)
            newFile.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误！"})
        return JsonResponse({'errno': 0, 'msg': "新建成功",'file_id':newFile.id})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def delete_file(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            file = Files.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "找不到该文件或目录！"})
        file.delete()
        return JsonResponse({'errno': 0, 'msg': "删除成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


def open_document(id):
    document = Document.objects.get(id=id)
    try:
        f = open(os.path.join(settings.MEDIA_ROOT, 'documents', document.data), 'r')
    except IOError as e:
        print(e)
        return JsonResponse({'errno': 2, 'msg': "文件已失效"})
    print("checked file")
    json = {
        'name': document.name,
        'url': DOCUMENTS_URL + document.data
    }
    return JsonResponse([json], safe=False)


def create_document(name, model_name, uid):
    if name == '':
        return JsonResponse({'errno': 2, 'msg': "名字不能为空"})
    try:
        user = Users.objects.get(id=uid)
    except:
        user = None
    now_time = datetime.datetime.now()
    file_name = now_time.strftime('%Y%m%d%H%M%S%f_') + 'xxx' + '_' + model_name
    if copy_file(model_name, file_name):
        return JsonResponse({'errno': 6666, 'msg': "文件创建失败"})
    try:
        document = Document(uid=user, data=file_name, name=name, create_time=now_time,
                            modify_time=now_time)
        document.save()
    except Exception as e:
        print(e)
        return JsonResponse({'errno': 9999, 'msg': "数据库存储出错了"})
    print("Aready saved in database")
    return JsonResponse({'errno': 0, 'msg': "创建成功", 'docid': document.id})

