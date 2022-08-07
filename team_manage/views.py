from django.http import JsonResponse
from django.core import serializers
from .models import *


def get_member(request):
    if request.method == 'POST':
        gid = request.POST.get('gid')
        if gid is None:
            return JsonResponse({'errno': 1002, 'msg': "参数为空，请检查参数名是否为\'gid\'"})
        try:
            members = Members.objects.filter(gid=gid)
            data = []
            for i in members:
                user = i.uid
                p_tmp = {
                    'id': user.id,
                    'username': user.username,
                    'role': i.field_role,
                    'avatar': str(user.avatar),
                    'name': user.name,
                    'email': user.email,
                    'gnum': user.gnum,
                    'profile': user.profile,
                }
                data.append(p_tmp)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "未知错误"})
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


def appoint(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        if gid is None or uid is None:
            return JsonResponse({'errno': 1002, 'msg': "uid或gid为空，请检查参数名是否为\'gid\',\'uid\'"})
        try:
            member = Members.objects.get(gid=gid, uid=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该用户或未知错误"})
        if member.field_role == 1:
            return JsonResponse({'errno': 1004, 'msg': "该用户已经为管理员！"})
        try:
            member.field_role = 1
            member.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1005, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "任命成功！"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


def delete(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        if gid is None or uid is None:
            return JsonResponse({'errno': 1002, 'msg': "uid或gid为空，请检查参数名是否为\'gid\',\'uid\'"})
        try:
            member = Members.objects.get(gid=gid, uid=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该用户或未知错误"})
        if member.field_role == 2:
            return JsonResponse({'errno': 1004, 'msg': "该用户为创建者，不能删除！"})
        try:
            member.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1005, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "删除成功！"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


def revoke(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        if gid is None or uid is None:
            return JsonResponse({'errno': 1002, 'msg': "uid或gid为空，请检查参数名是否为\'gid\',\'uid\'"})
        try:
            member = Members.objects.get(gid=gid, uid=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该用户或未知错误"})
        if member.field_role == 0:
            return JsonResponse({'errno': 1004, 'msg': "该用户不是管理员"})
        if member.field_role == 2:
            return JsonResponse({'errno': 1004, 'msg': "该用户是创建者，不能撤销"})
        try:
            member.field_role = 0
            member.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1005, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "撤销成功！"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


def get_user(request):
    if request.method == 'GET':
        users = Users.objects.all()
        data = []
        for user in users:
            member = Members.objects.filter(uid=user)
            team = []
            for i in member:
                team.append(i.gid.id)
            p_tmp = {
                'id': user.id,
                'username': user.username,
                'avatar': str(user.avatar),
                'name': user.name,
                'email': user.email,
                'gnum': user.gnum,
                'profile': user.profile,
                'team': team
            }
            data.append(p_tmp)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


def invite(request):
    if request.method == 'POST':
        invitee = request.POST.get('invitee')
        inviter = request.POST.get('inviter')
        gid = request.POST.get('gid')
        try:
            gid = Groups.objects.get(id=gid)
            invitee = Users.objects.get(id=invitee)
            inviter = Users.objects.get(id=inviter)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "不存在该用户或团队"})
        try:
            member = Members.objects.get(gid=gid, uid=invitee)
        except:
            pass
        else:
            return JsonResponse({'errno': 1004, 'msg': "该用户已在团队中"})
        try:
            newInvite = Invite(inviter=inviter.id,invitee=invitee.id,gid=gid.id,read=0)
            newInvite.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1005, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "已发送邀请，请等待回复"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def get_invitation(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        if uid is None:
            return JsonResponse({'errno':1002,'msg':"参数为空"})
        invitation = Invite.objects.filter(invitee=uid)
        data = []
        for i in invitation:
            try:
                group = Groups.objects.get(id=i.gid)
                name = group.name
            except Exception as e:
                print(e)
                name = '团队已被解散'
            tmp = {
                'id':i.id,
                'inviter':i.inviter,
                'invitee':i.invitee,
                'gid':i.gid,
                'gname':name,
            }
            data.append(tmp)
        return JsonResponse(data)
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def accept_invitation(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            invition = Invite.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1002, 'msg': "邀请不存在或已被删除"})
        uid = invition.invitee
        gid = invition.gid
        try:
            user = Users.objects.get(id=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "用户不存在"})
        try:
            group = Groups.objects.get(id=gid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': 1003, 'msg': "团队不存在或已被删除"})
        if Members.objects.filter(gid=group,uid=user).exists():
            return JsonResponse({'errno': 1004, 'msg': "你已加入该团队"})
        try:
            newMember = Members(gid=group,uid=user,field_role=2)
            newMember.save()
        except:
            return JsonResponse({'errno': 1005, 'msg': "未知错误"})
        else:
            return JsonResponse({'errno': 0, 'msg': "已成功加入团队"+"\'"+group.name+"\'"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

