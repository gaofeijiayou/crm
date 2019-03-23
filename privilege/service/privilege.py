
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect,render
import re
class MyPrivilege(MiddlewareMixin):

    def process_request(self, request):

        whitelist = ['/login/', '/reg/', '/admin/','/zhuxiao/', '/Xadmin/privilege/role/view/',
                     '/Xadmin/privilege/role/edit/(\d)', '/Xadmin/privilege/role/add/',
                     '/Xadmin/privilege/privilege/edit/(\d)', '/Xadmin/privilege/privilege/add/',
                     '/Xadmin/privilege/rolegroup/add/',
                     ]

        cru_url = request.path_info

        for url in whitelist:

            ret = re.match(url, cru_url)
            if ret:
                return None
        #校验是否登录

        user_id = request.session.get('user_id')
        next_url = request.GET.get('next')

        if not user_id:
            login_str = '/login/?next={}'.format(cru_url)
            return redirect(login_str)

        privi_list = request.session.get('pri_dic')

        for pri in privi_list.values():
            urls = pri['urls']
            for reg in urls:

                reg = '%s$'%reg
                ret = re.match(reg, cru_url)
                if ret:
                    request.action = pri['action']
                    return None

        return HttpResponse('没有权限')






def initial_session(user, re):


    per = user.role.all().values('privilege__title','privilege__rolegroup_id', 'privilege__action')
    #.values('privilege__title','privilege__rolegroup_id', 'privilege__action')

    pre_dic = {}

    for it in per:
        gid = it.get('privilege__rolegroup_id')
        if not gid in pre_dic:
            pre_dic[gid]={
                'urls':[it['privilege__title'],],
                'action':[it['privilege__action'],]
            }
        else:
            pre_dic[gid]['urls'].append(it[ 'privilege__title'])
            pre_dic[gid]['action'].append(it['privilege__action'])

    re.session['pri_dic'] = pre_dic

    show_men = user.role.all().values('privilege__rolegroup__title', 'privilege__action', 'privilege__title').distinct()
    men_list = []
    print(show_men)
    for it in show_men:
        if it['privilege__action'] == 'view':
            men_list.append((it['privilege__title'], it['privilege__rolegroup__title']))

    new_list = []
    i = 0
    item = None
    for k in show_men:
        if i == 0:
            print(k['privilege__rolegroup__title'])
            item = k['privilege__rolegroup__title']
            i = 1
        else:
            print(k['privilege__rolegroup__title'])
            print(item)
            i = 0


    print(men_list)
    re.session['men_list'] = men_list
    # privi_list = []
    #
    # re.session['user_id'] = user.pk
    # roles = user.role_set.all().values('privilege__title')
    #
    # for pre in roles:
    #     privi_list.append(pre['privilege__title'])
    #
    # re.session['privi_list'] = privi_list



[('/Xadmin/crms9/customer/view/', '客户管理'),
 ('/Xadmin/crms9/consultrecord/view/', '客户跟进记录管理'),
 ('/Xadmin/crms9/classlist/view/', '班级管理'),
 ('/Xadmin/crms9/userinfo/view/', '用户管理'),
 ('/Xadmin/crms9/courserecord/view/', '上课记录表'),
 ('/Xadmin/crms9/department/view/', '部门管理')]

[('/Xadmin/crms9/customer/view/', '客户管理'), ('/Xadmin/crms9/classlist/view/', '班级管理'), ('/Xadmin/crms9/consultrecord/view/', '客户跟进记录管理'), ('/Xadmin/crms9/userinfo/view/', '用户管理'), ('/Xadmin/crms9/department/view/', '部门管理'), ('/Xadmin/crms9/courserecord/view/', '上课记录表')]
