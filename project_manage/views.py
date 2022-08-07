from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import *
from com.funcs import *


@csrf_exempt
def get_project(request):
    if request.method == 'GET':
        gid = request.GET.get('gid')
        if gid is None:
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
        if gid is None or uid is None or name is None:
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
        else:
            return JsonResponse({'errno': 0, 'msg': "创建成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def rename(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        if id is None or name is None:
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
        else:
            return JsonResponse({'errno': 0, 'msg': "重命名成功"})
    else:
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
        else:
            return JsonResponse({'errno': 0, 'msg': "已移至回收站"})
    else:
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
        else:
            return JsonResponse({'errno': 0, 'msg': "已移出回收站"})
    else:
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
        else:
            return JsonResponse({'errno': 0, 'msg': "删除成功"})
    else:
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
def save_document(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        name = request.POST.get('name')
        file = request.FILES.get('file')
        try:
            new_document = Document(pid=pid, name=name, data=file)
            new_document.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1002, 'msg': "未知错误"})
        return JsonResponse({'errno': 0, 'msg': "保存成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_document(request):
    if request.method == 'GET':
        pid = request.GET.get('pid')
        if pid is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空"})
        docs = Document.objects.filter(pid=pid)
        data = []
        for d in docs:
            tmp = {
                'id': d.id,
                'name': d.name,
            }
            data.append(tmp)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def store_document(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        data = request.POST.get('data')
        try:
            document = Document.objects.get(id=id)
        except:
            return JsonResponse({'errno': 2, 'msg': "文件不存在"})
        else:
            document.data = data
            document.save()
            return JsonResponse({'errno': 0, 'msg': "修改成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def create_document(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        name = request.POST.get('name')
        data = request.POST.get('data')
        document = Document(pid=pid, name=name, data=data)
        document.save()
        return JsonResponse({'errno': 0, 'msg': "创建成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_documents(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        documents = Document.objects.filter(pid=pid)
        data = []
        for i in documents:
            tmp = {
                'id': i.id,
                'name': i.name,
                'pid': i.pid,
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
        return JsonResponse({'errno': 0, 'data': document.data})
        #  return prototype_serialize([prototype])
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
