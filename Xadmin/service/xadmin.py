__author__ = 'Administrator'
from django.shortcuts import HttpResponse, render, redirect
from django.urls import path, re_path
from django.db.models import Q
from django.utils.safestring import mark_safe
from Xadmin import models
from django.db.models.fields.related import ManyToManyRel,ManyToManyField
import datetime
class ShowList(object):
    def __init__(self, ConObj, re):
        self.conobj = ConObj
        self.re = re

    def get_head(self):
        head_list = []
        if hasattr(self.conobj, 'head_list'):
            for field in self.conobj.head_list:
                head_list.append(field)

        return head_list

    def get_serch_filter(self):

        import copy
        serch_filter = copy.deepcopy(self.re.GET)
        if 'page' in serch_filter.keys():
            del serch_filter['page']
        serch_q = Q()
        for se,v in serch_filter.items():

            serch_q.children.append((se.lower(),v))

        return  serch_q


    def get_filter_linktage(self):
        list_link = {}

        import copy

        if hasattr(self.conobj, 'list_filter'):

            for model_name, filter_name in self.conobj.list_filter.items():
                par = copy.deepcopy(self.re.GET)
                pid = self.re.GET.get(model_name)
                obj = getattr(models,model_name)
                temp = []

                if par.get(model_name):
                    del par[model_name]
                    temp.append("<a href='?{}'>全部</a>".format(par.urlencode()))
                else:
                    temp.append("<a href='#'>全部</a>")

                for o in obj.objects.all():

                    par[model_name] = o.pk

                    urlstr = par.urlencode()

                    if str(o.pk) == pid:

                        str1 = '<a class="btn btn-primary" href="?{}">{}</a>'.format(urlstr, o)
                    else:
                        str1 = '<a class="" href="?{}">{}</a>'.format(urlstr, o)
                    temp.append(str1)
                list_link[filter_name] = temp

        return list_link

    def action_list(self, modelobj):
        temp = []
        if hasattr(modelobj, 'action_list'):
            for act in modelobj.action_list:
                temp.append({
                    'dec_name':act.dec_name,
                    'fnc':act.__name__
                })

        return temp

    def get_ser_q(self):
        import copy
        serch_filter = copy.deepcopy(self.re.GET)

        if 'page' in serch_filter.keys():
            del serch_filter['page']

        key_word = serch_filter.get('q', 0)

        serch_q = Q()
        if key_word:
            serch_q.connector = 'or'
            print(self.conobj.serch_list)
            for serch_fleld in self.conobj.serch_list:
                serch_q.children.append((serch_fleld, key_word))
        return serch_q

    def get_body(self, model, data_list, new_list_display):
        new_list_data = []
        for obj in data_list:
            temp = []
            for filed in new_list_display():
                print(filed)
                if callable(filed):
                    temp.append(filed(model, obj))
                else:
                    try:
                        filed_obj = self.conobj.model._meta.get_field(filed)
                        if isinstance(filed_obj, ManyToManyField):
                            t =[]
                            var = getattr(obj, filed).all()
                            for v in var:
                                t.append(str(v))
                            temp.append(','.join(t))
                        elif isinstance(filed_obj, ManyToManyRel):
                            model_name = self.conobj.model._meta.model_name
                            many_obj = self.conobj.model.objects.filter(pk=obj.pk).first()
                            obj_set = getattr(many_obj, filed+'_set')
                            many_obj = obj_set.all()
                            item = []
                            for m in many_obj:
                                item.append(str(m))
                            temp.append(','.join(item))
                        else:
                            if filed_obj.choices:
                                var = getattr(obj, "get_"+filed+'_display')()
                                temp.append(var)

                            else:
                                temp.append(str(getattr(obj, filed)))
                    except Exception  as msg:
                        print(msg)
            new_list_data.append(temp)

        return new_list_data


class ModelXadmin(object):
    modelform_class = None
    def __init__(self, model, site):
        self.model = model
        self.site = site


    list_display = ['__str__']
    def checkbox(self, obj):

        return mark_safe('<input type="checkbox" class="BodyCheckbox" value="{}" name="select"'.format(obj.pk))

    def change(self, obj=None, head=False):

        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        url = '/Xadmin/{}/{}/edit/{}'.format(app_label, model_name, obj.pk)

        return mark_safe("<a class='btn btn-info' href='{}'>编辑</a>".format(url))

    def delete(self, obj=None, head=False):

        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        url = '/Xadmin/{}/{}/del/{}'.format(app_label, model_name, obj.pk)

        return mark_safe("<a class='btn btn-warning' href='{}'>删除</a>".format(url))

    def get_add_url(self):
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label

        return "/Xadmin/{}/{}/add/".format(app_name,model_name)

    def get_del_url(self):
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label

        return "/Xadmin/{}/{}/del/".format(app_name,model_name)

    def get_view_url(self):
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label

        return "/Xadmin/{}/{}/view/".format(app_name,model_name)

    def get_edit_url(self):
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label

        return "/Xadmin/{}/{}/edit/".format(app_name,model_name)

    def get_modelform_class(self):

        if not self.modelform_class:
            from django.forms import ModelForm
            from django.forms import widgets as wid
            class ModelFormDemo(ModelForm):
                class Meta:
                    model = self.model
                    fields = "__all__"
                    labels={
                        ""
                    }
            return ModelFormDemo
        else:
            return self.modelform_class


    def add(self, re):

        model_form = self.get_modelform_class()
        form = model_form()
        if re.method == 'POST':
            form = model_form(re.POST)
            if form.is_valid():
                obj = form.save()
                pop_id = re.GET.get('pop_id')
                if not hasattr(obj, 'code'):
                    obj.code = None

                if pop_id:
                    res={'select': pop_id, 'title': str(obj), 'pid': obj.pk, 'code': obj.code}
                    import json

                    return render(re, 'pop.html', {'res':res})
                else:
                    return redirect(self.get_view_url())
        from django.forms.models import ModelChoiceField
        for i in form:
            if isinstance(i.field, ModelChoiceField):
                i.is_pop = True
                model_name = i.field.queryset.model._meta.model_name
                app_name = i.field.queryset.model._meta.app_label
                i.addurl = '/Xadmin/{}/{}/add/'.format(app_name, model_name,)

        return render(re, 'add.html', locals())

    def dele(self, re, pid):
        self.model.objects.filter(pk=pid).delete()

        return redirect(self.get_view_url())

    def edit(self, re, pid):

        obj = self.model.objects.filter(pk=pid).first()
        model_form = self.get_modelform_class()

        if re.method == 'POST':
            form = model_form(re.POST, instance=obj)

            if form.is_valid():
                form.save()
                return redirect(self.get_view_url())

        form = model_form(instance=obj)
        return render(re, 'edit.html', locals())

    def new_list_display(self):
        temp = []
        temp.append(ModelXadmin.checkbox)
        temp.extend(self.list_display)
        temp.append(ModelXadmin.delete)
        temp.append(ModelXadmin.change)


        return temp

    def view(self, re):
        #获取当前的页码
        from Xadmin.service.page import Pagination
        show_list =ShowList(self, re)
        if re.method == 'POST':
            fnc = re.POST.get('select_action', 0)
            if fnc:
                action_fnc = getattr(self, fnc)
                select = re.POST.getlist('select')
                query_set = self.model.objects.filter(pk__in=select)
                action_fnc(re, query_set)

        serch_q = show_list.get_serch_filter()

        #serch_q = show_list.get_ser_q()

        count = self.model.objects.all().filter(serch_q).count()

        page = Pagination(re, count)

        action_list = show_list.action_list(self)

        get_filter_linktage = show_list.get_filter_linktage()

        data_list = self.model.objects.all().filter(serch_q)[page.start_index: page.end_index]

        new_list_data = show_list.get_body(self, data_list, self.new_list_display)

        head_list = show_list.get_head()

        add_url = self.get_add_url()

        print(3434)
        return render(re, 'view.html', locals())

    def extra_url(self):
        temp =[]

        return temp

    def get_urls2(self):
            temp = []
            temp.append(path('add/', self.add))
            temp.append(re_path('del/(\d+)', self.dele))
            temp.append(path('view/', self.view))
            temp.append(re_path('edit/(\d+)', self.edit))
            temp.extend(self.extra_url())


            return temp


    @property
    def urls_2(self):
            return self.get_urls2(), None, None


class XadminSite():
    def __init__(self):
        self._register = {}

    def get_urls(self):
        temp = []

        for model, admin_class in self._register.items():
            model_name = model._meta.model_name
            app_label = model._meta.app_label

            temp.append(path('{}/{}/'.format(app_label, model_name), admin_class.urls_2))
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None

    def register(self, model, admin_class=None):
        if not admin_class:
            admin_class = ModelXadmin

        self._register[model] = admin_class(model, self)


Xadmin = XadminSite()





