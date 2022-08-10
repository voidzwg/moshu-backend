from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from moshu import settings
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
                if p.uid is None:
                    uid = None
                else:
                    uid = p.uid.id
                tmp = {
                    'id': p.id,
                    'name': p.name,
                    'available': p.available,
                    'status': p.status,
                    'gid': p.gid.id,
                    'uid': uid,
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
            group = Groups.objects.get(id=gid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该团队"})
        try:
            user = Users.objects.get(id=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该用户"})
        try:
            newProject = Projects(gid=group,uid=user,name=name, starttime=datetime.datetime.now(), available=0, status=0)
            newProject.save()
            Group_root = Files.objects.get(name=gid)
            Group_Project_root = Group_root.get_children()[0]
            project_root = str(group.id)+'_project_'+str(newProject.id)+'_'+newProject.name
            new_project_root = Files(name=project_root,isfile=0,parent=Group_Project_root)
            new_project_root.save()
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
        if delete_project_file(project):
            print("cannot delete project files")
            return JsonResponse({'errno': 1005, 'msg': "未知错误"})
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
        try:
            group = Groups.objects.get(id=project.gid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 2333, 'msg': "不存在项目所属的团队"})
        new_project_name = project.name + " - 副本"
        now_time = datetime.datetime.now()
        try:
            new_project = Projects(gid=group, uid=user, name=new_project_name, starttime=now_time,
                                   endtime=project.endtime, available=0, status=0, profile=project.profile)
            new_project.save()
            prototype = Prototype.objects.filter(pid=project)
            for p in prototype:
                new_prototype_name = rename_project_file(now_time, new_project.id, p.name)
                copy_file(p.name, new_prototype_name)
                new_prototype = Prototype(name=new_prototype_name, pid=new_project, create_time=now_time,
                                          modify_time=now_time, data=p.data, width=p.width, height=p.height)
                new_prototype.save()
            document = Document.objects.filter(pid=project)
            for d in document:
                new_document_name = rename_project_file(now_time, new_project.id, d.name)
                copy_file(d.name, new_document_name)
                new_document = Document(name=new_document_name, pid=new_project, uid=user,
                                        create_time=now_time, modify_time=now_time, data=d.data)
                new_document.save()
            uml = Uml.objects.filter(pid=project.id)
            for u in uml:
                new_uml_name = rename_project_file(now_time, new_project.id, u.name)
                copy_file(u.name, new_uml_name)
                new_uml = Uml(name=new_uml_name, pid=new_project, uid=user,
                              create_time=now_time, modify_time=now_time, data=u.data)
                new_uml.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1004, 'msg': "未知错误"})
        return JsonResponse({'errno': 0, 'msg': "复制成功"})
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def store_document(request):
    print("IN STORE_DOCUMENT")
    if request.method == 'POST':
        print("IN IF")
        try:
            doc_id = request.POST.get('id')
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 3333, 'msg': "未知错误"})
        print("Out of try")
        print("type of doc_id", type(doc_id))
        file_str = request.FILES.get('file')
        print("File String", file_str)
        print("type of file_str", type(file_str))
        try:
            document = Document.objects.get(id=doc_id)
        except:
            return JsonResponse({'errno': 2, 'msg': "文档不存在"})
        print("Already checked document")
        if store_file(file_str, document.data):
            return JsonResponse({'errno': 6667, 'msg': "存储失败"})
        document.modify_time = datetime.datetime.now()
        document.save()
        print("Already saved in database")
        return JsonResponse({'errno': 0, 'msg': "修改成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
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
        try:
            project_root_name = str(project.gid.id) + '_Project_' + str(project.id) + '_' + project.name
            project_root = Files.objects.get(name=project_root_name)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 7777, 'msg': "未获取到根目录"})
        try:
            document_name = project_root_name + '_' + str(document.id) + '_' + document.name
            new_project_root = Files(name=document_name, isfile=1, parent=project_root, document=document)
            new_project_root.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 7777, 'msg': "加入文件系统失败"})
        print("Aready saved in database")
        return JsonResponse({'errno': 0, 'msg': "创建成功并已同步至文档中心", 'docid': document.id})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_documents(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        try:
            project = Projects.objects.get(id=pid)
        except:
            return JsonResponse({'errno': 2, 'msg': "项目不存在"})
        documents = Document.objects.filter(pid=project)
        data = []
        for i in documents:
            if i.uid is None:
                username = None
                creator = None
            else:
                username = i.uid.username
                creator = i.uid.name
            tmp = {
                'id': i.id,
                'name': i.name,
                'pid': i.pid.id,
                'create_time': i.create_time,
                'modify_time': i.modify_time,
                'creator_username': username,
                'creator':creator,
            }
            data.append(tmp)
        return JsonResponse(data, safe=False)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def open_document(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print("begin")
        try:
            document = Document.objects.get(id=id)
        except:
            return JsonResponse({'errno': 2, 'msg': "文件不存在"})
        print("checked document")
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
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def delete_document(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            doc = Document.objects.get(id=id)
        except:
            return JsonResponse({'errno': 2, 'msg': "文件不存在"})
        if delete_file(DOCUMENTS_URL + doc.data):
            return JsonResponse({'errno': 6668, 'msg': "文件不存在"})
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
