import base64
import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from com.funcs import *


# Author: zwg
# Create your views here.
@csrf_exempt
def store(request):
    if request.method == 'POST':
        picid = request.POST.get('picid')
        # print("type of picid", type(picid))
        file_str = request.FILES.get('file')
        # print("type of file_str", type(file_str))
        try:
            prototype = Prototype.objects.get(id=picid)
        except:
            return JsonResponse({'errno': 2, 'msg': "原型设计不存在"})
        if store_file(file_str, prototype.data):
            return JsonResponse({'errno': 6667, 'msg': "存储失败"})
        prototype.modify_time = datetime.datetime.now()
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
        if copy_file(model_name, file_name):
            return JsonResponse({'errno': 6666, 'msg': "文件创建失败"})
        prototype = Prototype(pid=project, uid=user, name=name, data=file_name, width=width, 
                              height=height, create_time=now_time, modify_time=now_time)
        prototype.save()
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
        if delete_file(DOCUMENTS_URL + prototype.data):
            return JsonResponse({'errno': 6668, 'msg': "文件不存在"})
        prototype.delete()
        return JsonResponse({'errno': 0, 'msg': "删除成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_design(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        try:
            project = Projects.objects.get(id=pid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 2, 'msg': "项目不存在"})
        prototype_list = Prototype.objects.filter(pid=project)
        return prototype_serialize(prototype_list)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_one_design(request):
    if request.method == 'POST':
        picid = request.POST.get('picid')
        try:
            prototype = Prototype.objects.get(id=picid)
        except:
            return JsonResponse({'errno': 2, 'msg': "原型设计不存在"})
        try:
            f = open(os.path.join(settings.MEDIA_ROOT, 'documents', prototype.data), 'r')
        except IOError as e:
            return JsonResponse({'errno': 2, 'msg': "文件已失效"})
        json = {
            'url': DOCUMENTS_URL + prototype.data,
            'name': prototype.name,
            'width': prototype.width,
            'height': prototype.height,
        }
        return JsonResponse([json], safe=False)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def upload_prototype(request):
    if request.method == 'POST':
        pic_id = request.POST.get('picid')
        base64_img = request.POST.get('img')
        try:
            prototype = Prototype.objects.get(id=pic_id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 2, 'msg': "原型设计不存在"})
        if base64_img is None:
            return JsonResponse({'errno': 1, 'msg': "参数错误"})
        img_split = base64_img.split('base64,')
        img_data = base64.b64decode(img_split[1])
        img_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f_') + str(pic_id) + '.png'
        if prototype.img:
            if delete_file(IMAGE_URL + prototype.img):
                print("Cannot find image named", prototype.img)
            else:
                print("Already delete old image", prototype.img)
        with open(os.path.join(settings.MEDIA_ROOT, 'images', img_name), 'wb') as img:
            img.write(img_data)
        print("Already create image named", img_name)
        prototype.img = img_name
        prototype.save()
        print("Already saved in database")
        return JsonResponse({'errno': 0, 'msg': "上传成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_prototype_img(request):
    if request.method == 'POST':
        pic_id = request.POST.get('picid')
        try:
            prototype = Prototype.objects.get(id=pic_id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 2, 'msg': "原型设计不存在"})
        if prototype.img:
            img_url = IMAGE_URL + prototype.img
        else:
            img_url = None
        return JsonResponse({'errno': 0, 'msg': "返回成功", 'url': img_url})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_show_status(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        try:
            project = Projects.objects.get(id=pid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 2, 'msg': "项目不存在"})
        return JsonResponse({'errno': 0, 'msg': "获取成功", 'showable': project.showable})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def change_show_status(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        try:
            project = Projects.objects.get(id=pid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 2, 'msg': "项目不存在"})
        project.showable = project.showable ^ 1
        project.save()
        return JsonResponse({'errno': 0, 'msg': "修改成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def search_design(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        try:
            project = Projects.objects.get(id=pid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 2, 'msg': "项目不存在"})
        keyword = request.POST.get('keyword')
        if keyword == '':
            return JsonResponse({'errno': 5, 'msg': "搜索内容不能为空！"})
        prototypes = Prototype.objects.filter(pid=project)
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