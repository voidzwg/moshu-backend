from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import *
from com.funcs import *


@csrf_exempt
def get_project(request):
    if request.method == 'GET':
        gid = request.GET.get('gid')
        if gid == '':
            return JsonResponse({'errno': 1002, 'msg': "参数为空，请检查参数名是否为\'gid\'"})
        try:
            projects = Projects.objects.filter(gid=gid)
            data = []
            for p in projects:
                tmp = {
                    'id': p.id,
                    'name': p.name,
                    'available': p.available,
                    'status': p.status,
                    'gid': p.gid.id,
                    'uid': p.uid.id,
                    'starttime': p.starttime,
                    'endtime': p.endtime,
                    'profile': p.profile,
                }
                data.append(tmp)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "未知错误"})
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def create(request):
    if request.method == 'POST':
        gid = request.POST.get('gid')
        uid = request.POST.get('uid')
        name = request.POST.get('name')
        if gid == '' or uid == '' or name == '':
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
        return JsonResponse({'errno': 0, 'msg': "创建成功"})
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def rename(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        if id == '' or name == '' or name is None:
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
        return JsonResponse({'errno': 0, 'msg': "重命名成功"})
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
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
            project.available = 1
            project.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误"})
        return JsonResponse({'errno': 0, 'msg': "已移至回收站"})
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def out_bin(request):
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
            project.available = 0
            project.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误"})
        return JsonResponse({'errno': 0, 'msg': "已移出回收站"})
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
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
        return JsonResponse({'errno': 0, 'msg': "删除成功"})
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
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
            project.status = 1
            project.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "项目结束成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def copy(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        uid = request.POST.get('uid')
        if id is None or uid is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            project = Projects.objects.get(id=id)
            user = Users.objects.get(id=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该项目"})
        num = Projects.objects.filter(name__contains=project.name).count()
        num = str(num)
        name = project.name+'('+num+')'
        try:
            newProject = Projects(gid= project.gid,uid=user,name=name,available=0,status=0,profile=project.profile)
            newProject.save()
            prototype = Prototype.objects.filter(pid=project.id)
            for p in prototype:
                name = p.name + '(' + num + ')'
                newPrototype = Prototype(name=name,pid=newProject.id,data=p.data,width=p.width,height=p.height)
                newPrototype.save()
            document = Document.objects.filter(pid=project.id)
            for d in document:
                name = d.name + '(' + num + ')'
                newDocument = Document(name=name, pid=newProject.id, data=d.data)
                newDocument.save()
            uml = Uml.objects.filter(pid=project.id)
            for u in uml:
                name = u.name + '(' + num + ')'
                newUml = Uml(name=name, pid=newProject.id, data=u.data)
                newUml.save()
        except Exception as e:
            return JsonResponse({'errno': 1004, 'msg': "未知错误"})
        return JsonResponse({'errno': 0, 'msg': "复制成功"})
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def store_document(request):
    if request.method == 'POST':
        doc_id = request.POST.get('id')
        # print("type of picid", type(picid))
        file_str = request.FILES.get('file')
        # print("type of file_str", type(file_str))
        try:
            document = Document.objects.get(id=doc_id)
        except:
            return JsonResponse({'errno': 2, 'msg': "原型设计不存在"})
        content = b''
        for ch in file_str.chunks():
            content += ch
        with open(os.path.join(settings.MEDIA_ROOT, 'documents', document.data), 'wt') as store_file:
            store_file.write(content.decode('utf-8'))
        document.modify_time = datetime.datetime.now()
        document.save()
        return JsonResponse({'errno': 0, 'msg': "修改成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def create_document(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        name = request.POST.get('name')
        model_name = request.POST.get('model_name')
        if name == '':
            return JsonResponse({'errno': 2, 'msg': "名字不能为空"})
        try:
            project = Projects.objects.get(id=pid)
        except:
            return JsonResponse({'errno': 2, 'msg': "项目不存在"})
        now_time = datetime.datetime.now()
        file_name = now_time.strftime('%Y%m%d%H%M%S%f_') + str(pid) + '_' + model_name
        content = ''
        with open(os.path.join(settings.MEDIA_ROOT, 'documents', model_name), 'rt') as model_file:
            while True:
                msg = model_file.read(READ_LENGTH)
                if msg == '':
                    break
                content += msg
        with open(os.path.join(settings.MEDIA_ROOT, 'documents', file_name), 'at') as new_file:
            while content:
                msg = content[:READ_LENGTH]
                new_file.write(msg)
                content = content[READ_LENGTH:]
        document = Document(pid=pid, data=file_name, name=name, create_time=now_time, modify_time=now_time)
        document.save()
        return JsonResponse({'errno': 0, 'msg': "创建成功", 'docid': document.id})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_documents(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        documents = Document.objects.filter(pid=pid)
        data = []
        for i in documents:
            if i.uid is None:
                username = None
            else:
                username = i.uid.username
            tmp = {
                'id': i.id,
                'name': i.name,
                'pid': i.pid,
                'create_time': i.create_time,
                'modify_time': i.modify_time,
                'creator_username': username
            }
            data.append(tmp)
        return JsonResponse(data, safe=False)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def open_document(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            document = Document.objects.get(id=id)
        except:
            return JsonResponse({'errno': 2, 'msg': "文件不存在"})
        try:
            f = open(os.path.join(settings.MEDIA_ROOT, 'documents', document.data), 'r')
        except IOError as e:
            return JsonResponse({'errno': 2, 'msg': "文件已失效"})
        json = {
            'name': document.name,
            'url': document.data
        }
        return JsonResponse([json], safe=False)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def delete_document(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            doc = Document.objects.get(id=id)
        except:
            return JsonResponse({'errno': 2, 'msg': "文件不存在"})
        doc.delete()
        return JsonResponse({'errno': 0, 'msg': "删除成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def rename_document(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        if id is None or name is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        try:
            document = Document.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "文件不存在"})
        if name == '':
            return JsonResponse({'errno': 1004, 'msg': "名称不能为空"})
        try:
            document.name = name
            document.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1005, 'msg': "未知错误"})
        return JsonResponse({'errno': 0, 'msg': "重命名成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def search_projects(request):
    if request.method == 'POST':
        gid = request.POST.get('gid')
        try:
            group = Groups.objects.get(id=gid)
        except:
            return JsonResponse({'errno': 4, 'msg': "团队不存在！"})

        keyword = request.POST.get('keyword')
        if keyword == '':
            return JsonResponse({'errno': 5, 'msg': "搜索内容不能为空！"})

        projects = Projects.objects.filter(gid=group)
        profile_list = []
        name_list = []
        for project in projects:
            name_list.append(project.name)
            if project.profile:
                profile_list.append(project.profile)
            else:
                profile_list.append('')
        choices_list = [name_list, profile_list]
        list_a = fuzzy_search(keyword, choices_list)
        results = []
        for key in list_a:
            filters = projects.filter(name=key[0])
            if filters:
                for item in filters:
                    results.append(item)
                continue

            filters = projects.filter(profile=key[0])
            if filters:
                for item in filters:
                    results.append(item)
                continue
        unique_results = list(set(results))
        unique_results.sort(key=results.index)
        return project_serialize(unique_results)
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

