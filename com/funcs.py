from django.http import JsonResponse
import re
from group_manage.models import Members

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


def space_serialize(user):
    data = []
    path = AVATAR_HOME + user.avatar
    try:
        avatar = open(path, 'r', encoding='UTF-8').read()
        print(avatar)
    except OSError as reason:
        print('读取文件出错了T_T')
        print('出错原因是%s' % str(reason))
        avatar = -1
    p_tmp = {
        'username': user.username,
        'name': user.name,
        'avatar': avatar,
        'email': user.email,
        'gnum': user.gnum,
        'profile': user.profile
    }
    data.append(p_tmp)
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
            return JsonResponse({'errno': 3, 'msg': "团队没有创建者"})
        json = {
            'username': uname,
            'gid': group.id,
            'name': group.name,
            'unum': group.unum
        }
        data.append(json)
    return JsonResponse(data, safe=False)

