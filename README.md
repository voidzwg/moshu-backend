# moshu-backend

## API

### 登录注册

登录：/api/login/login/

注册：/api/login/register/

### 个人信息页面

获取个人信息：/api/space/get_info/

修改个人信息：/api/space/update_info/

修改密码：/space/api/update_password/

获取已加入团队名称：/api/space/get_group/

头像上传： /api/space/set_avatar/

### 管理团队页面

获取成员信息： /api/team_manage/get_member/

任命管理员： /api/team_manage/appoint/

删除成员： /api/team_manage/delete/

撤销管理员： /api/team_manage/revoke/

### 邀请页面

获取所有成员： /api/team_manage/get_user/

邀请该成员进入该团队: /api/team_manage/invite/

### 管理项目页面

获取团队的所有项目： /api/project_manage/get_project/

新建项目： /api/project_manage/create/

重命名项目：/api/project_manage/rename/

移动项目至回收站：/api/project_manage/to_bin/

将项目移出回收站：/api/project_manage/out_bin/

删除项目：/api/project_manage/delete/

结束项目：/api/project_manage/close/

复制项目： /api/project_manage/copy/

保存文件：/api/project_manage/save_document/  参数： pid name file

获取文件： /api/project_manage/get_document/  参数：pid         请求方式：GET

打开文件： /api/project_manage/open_document/  参数： id

重命名文件：/api/project_manage/rename_document/ 参数： id name

文档上传图片：/api/project_manage/upload_img/   参数：did  img  formData打包

模糊搜索项目：/api/project_manage/search_projects/

### 团队管理页面

新建团队：/api/group_manage/create_group/

获取创建团队信息：/api/group_manage/get_created_group/

获取管理团队信息：/api/group_manage/get_managed_group/

获取参与团队信息：/api/group_manage/get_participated_group/

解散团队： /api/group_manage/dismiss/

模糊搜索用户：/api/group_manage/search_users/

### 原型设计页面

存储设计图数据：/api/design/store/

重命名设计图：/api/design/rename/

创建设计图：/api/design/create/

删除设计图：/api/design/delete/

获取设计图数据：/api/design/get_design/

模糊搜索设计图：/api/design/search_design/

获取模板信息：/api/design/get_templates/   GET

打开模板： /api/design/open_template/   POST parameters: id

存储原型设计预览图：/api/design/upload_prototype/

获取原型设计预览图：/api/design/get_prototype_img/

查看项目预览状态：/api/design/get_show_status/

改变项目预览状态：/api/design/change_show_status/

