from Xadmin.service.xadmin import *
from privilege import models
class UserCon(ModelXadmin):
    head_list = ['账户名','拥有角色']
    list_display = ['username', 'role']
Xadmin.register(models.User, UserCon)

class RoleCon(ModelXadmin):
    head_list = ['角色名','拥有的权限']
    list_display = ['title', 'privilege']
Xadmin.register(models.Role, RoleCon)

class PriviCon(ModelXadmin):
    head_list = ['权限路径','动作', '所属组']
    list_display = ['title', 'action', 'rolegroup']
Xadmin.register(models.Privilege, PriviCon)

class RoleCon(ModelXadmin):
    head_list = ['角色名']
    list_display = ['title']
Xadmin.register(models.Role, RoleCon)

class GoleGroupCon(ModelXadmin):
    head_list = ['标题']
    list_display = ['title']
Xadmin.register(models.RoleGroup, GoleGroupCon)

