from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from com.funcs import *
from .models import *


# Author: zwg
# Create your views here.
@csrf_exempt
def create_group(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        name = request.POST.get('name')
        if name is None:
            return JsonResponse({'errno': 2, 'msg': "名字不能为空"})
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 3, 'msg': "用户不存在"})
        new_groups = Groups(name=name, unum=1, pnum=0)
        new_groups.save()
        new_members = Members(gid=new_groups, uid=user, field_role=2)
        new_members.save()
        return JsonResponse({'errno': 0, 'msg': "创建成功"})
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_created_group(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 3, 'msg': "用户不存在"})
        members = Members.objects.filter(uid=user, field_role=2)
        group_list = []
        for member in members:
            group_list.append(member.gid)
        return group_serialize(group_list)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_managed_group(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 3, 'msg': "用户不存在"})
        members = Members.objects.filter(uid=user, field_role=1)
        group_list = []
        for member in members:
            group_list.append(member.gid)
        return group_serialize(group_list)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def get_participated_group(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        try:
            user = Users.objects.get(id=uid)
        except:
            return JsonResponse({'errno': 3, 'msg': "用户不存在"})
        members = Members.objects.filter(uid=user, field_role=0)
        group_list = []
        for member in members:
            group_list.append(member.gid)
        return group_serialize(group_list)
    return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def dismiss(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        if uid is None or gid is None:
            return JsonResponse({'errno': 1002, 'msg': "uid或gid为空，请检查参数名是否为\'gid\',\'uid\'"})
        try:
            member = Members.objects.get(gid=gid, uid=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在或未知错误"})
        if member.field_role != 2:
            return JsonResponse({'errno': 1004, 'msg': "不是创建者，不能解散团队！"})
        else:
            try:
                group = Groups.objects.get(id=gid)
            except Exception as e:
                print(e)
                return JsonResponse({'errno': 1003, 'msg': "不存在或未知错误"})
            else:
                group.delete()
                return JsonResponse({'errno': 0, 'msg': "解散成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def search_users(request):
    if request.method == 'POST':
        gid = request.POST.get('gid')
        try:
            group = Groups.objects.get(id=gid)
        except:
            return JsonResponse({'errno': 4, 'msg': "团队不存在！"})

        members = Members.objects.filter(gid=group)
        uid_list = []
        for member in members:
            uid_list.append(member.uid.id)

        keyword = request.POST.get('keyword')
        if keyword == '':
            return JsonResponse({'errno': 5, 'msg': "搜索内容不能为空！"})

        users = Users.objects.all()
        users.filter(id__in=uid_list).delete()
        username_list = email_list = name_list = []
        for user in users:
            username_list.append(user.username)
            name_list.append(user.name)
            email_list.append(user.email)
        choices_list = [username_list, email_list]
        list_a = fuzzy_search('void', choices_list)
        results = []
        for key in list_a:
            filters = users.filter(username=key[0])
            if filters:
                results.append(filters[0])
                continue

            filters = users.filter(name=key[0])
            if filters:
                for item in filters:
                    results.append(item)
                continue

            filters = users.filter(email=key[0])
            if filters:
                for item in filters:
                    results.append(item)
                continue
        unique_results = list(set(results))
        unique_results.sort(key=results.index)
        return users_serialize(unique_results)
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

