from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField('用户名', max_length=32)
    password = models.CharField('用户密码', max_length=32)
    role = models.ManyToManyField(to='role')
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name
class Role(models.Model):

    title = models.CharField('角色', max_length=12)
    privilege = models.ManyToManyField(to='Privilege')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "角色管理"
        verbose_name_plural = verbose_name

class Privilege(models.Model):

    title = models.CharField(max_length=64)
    action = models.CharField(max_length=32, default=1)
    rolegroup = models.ForeignKey('rolegroup', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "权限管理"
        verbose_name_plural = verbose_name

class RoleGroup(models.Model):

    title = models.CharField(max_length=32)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "权限角色组"
        verbose_name_plural = verbose_name


