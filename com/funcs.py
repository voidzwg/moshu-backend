from django.http import JsonResponse
import re
from group_manage.models import Members
from fuzzywuzzy import process

DEFAULT_AVATAR = "111"  # 默认头像文件名
AVATAR_HOME = "../static/avatars/"  # 头像文件存放地址


def check_email(email):
    if email == "":
        return True
    ex_email = re.compile(r'^[\w]+@[\w.]+com|net|cn')
    result = ex_email.match(email)
    if result:
        return True
    return False


# 必须包含字母和数字，且长度在8和18之间，否则为非法，返回False
def check_password(password):
    check_alpha = True
    check_digit = True
    check_len = True
    length = 0
    for ch in password:
        length += 1
        if '0' <= ch <= '9' or 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
            if '0' <= ch <= '9':
                check_digit = False
            if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
                check_alpha = False
        else:
            check_alpha = check_digit = True
            break
    if 8 <= length <= 18:
        check_len = False
    if check_alpha or check_digit or check_len:
        return False
    return True


def user_serialize(user):
    data = []
    p_tmp = {
        'username': user.username,
        'name': user.name,
        'avatar': str(user.avatar),
        'email': user.email,
        'gnum': user.gnum,
        'profile': user.profile
    }
    data.append(p_tmp)
    return JsonResponse(data, safe=False)


def users_serialize(user_list):
    data = []
    for user in user_list:
        json = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'avatar': str(user.avatar),
            'email': user.email,
            'gnum': user.gnum,
            'profile': user.profile
        }
        data.append(json)
    return JsonResponse(data, safe=False)


def group_serialize(group_list):
    data = []
    for group in group_list:
        members = Members.objects.filter(gid=group)
        uname = ''
        for member in members:
            if member.field_role == 2:
                uname = member.uid.username
        if uname == '':
            print("团队没有创建者")
        json = {
            'username': uname,
            'gid': group.id,
            'name': group.name,
            'unum': group.unum
        }
        data.append(json)
    return JsonResponse(data, safe=False)


def project_serialize(project_list):
    data = []
    for project in project_list:
        if project.uid:
            uid = project.uid.id
        else:
            uid = None
        json = {
            'id': project.id,
            'name': project.name,
            'available': project.available,
            'status': project.status,
            'gid': project.gid.id,
            'uid': uid,
            'starttime': project.starttime,
            'endtime': project.endtime,
            'profile': project.profile
        }
        data.append(json)
    return JsonResponse(data, safe=False)


def prototype_serialize(prototype_list):
    data = []
    for prototype in prototype_list:
        json = {
            'picid': prototype.id,
            'data': prototype.data,
            'name': prototype.name
        }
        data.append(json)
    return JsonResponse(data, safe=False)


# 将两个有序元组列表合并为一个新的有序元组列表
# list_a, list_b: 形如 [('name', 40), ('ame', 30)] 等模式的列表（字符串和相似度组成的元组的列表），按相似度降序排列
def merge_list(list_a, len_a, list_b, len_b):
    i = j = 0
    results = []
    while i < len_a and j < len_b:
        if list_a[i][1] >= list_b[j][1]:
            results.append(list_a[i])
            i += 1
        else:
            results.append(list_b[j])
            j += 1
    results += list_a[i:] + list_b[j:]
    return results


# 从 choices_list 表中查找模糊匹配键值 key 的元素
# choices_list: 形如 [['a', 'b', 'c'], ['k', 'p'], ['114', '514']] 等模式的列表（字符串的列表的列表）
def fuzzy_search(key, choices_list):
    results = []
    for choices in choices_list:
        choices_results = process.extract(key, choices, limit=10)
        results = merge_list(results, len(results), choices_results, len(choices_results))
    return results

