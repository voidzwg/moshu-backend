# moshu-backend

## API

### 登录注册

登录：http://127.0.0.1:8000/api/login/login/

注册：http://127.0.0.1:8000/api/login/register/

### 个人信息页面

获取个人信息：http://127.0.0.1:8000/api/space/get_info/

修改个人信息：http://127.0.0.1:8000/api/space/update_info/

修改密码：http://127.0.0.1:8000/space/api/update_password/

获取已加入团队名称：http://127.0.0.1:8000/api/space/get_group/

### 管理团队页面

获取成员信息： http://127.0.0.1:8000/api/team_manage/get_member/

任命管理员： http://127.0.0.1:8000/api/team_manage/appoint/

删除成员： http://127.0.0.1:8000/api/team_manage/delete/

撤销管理员： http://127.0.0.1:8000/api/team_manage/revoke/

### 邀请页面

获取所有成员： http://127.0.0.1:8000/api/team_manage/get_user/

邀请该成员进入该团队: http://127.0.0.1:8000/api/team_manage/invite/

### 管理项目页面

获取团队的所有项目： http://127.0.0.1:8000/api/project_manage/get_project/

新建项目： http://127.0.0.1:8000/api/project_manage/create/

重命名项目：http://127.0.0.1:8000/api/project_manage/rename/

移动项目至回收站：http://127.0.0.1:8000/api/project_manage/to_bin/

删除项目：http://127.0.0.1:8000/api/project_manage/delete/

结束项目：http://127.0.0.1:8000/api/project_manage/close/

### 团队管理页面

新建团队：http://127.0.0.1:8000/api/group_manage/create_group/

获取创建团队信息：http://127.0.0.1:8000/api/group_manage/get_created_group/

获取管理团队信息：http://127.0.0.1:8000/api/group_manage/get_managed_group/

获取参与团队信息：http://127.0.0.1:8000/api/group_manage/get_participated_group/

