from django.contrib import admin
from Xadmin.service.xadmin import Xadmin,ModelXadmin
from crms9.models import *
from django.shortcuts import HttpResponse, render, redirect
from django.utils.safestring import mark_safe
from django.urls import path, re_path
from django.db.models import Q
# Register your models here.
#     list_display = ['id', 'title', 'price', 'auth', 'cbs']
#     serch_list = ['title', 'price']
#     head_list = ['id', '书名', '价钱', '作者', '出版社']
#
#     Modelform_class = BookForm
#     list_filter = {'Cbs':'出版社', 'Auth':'作者'}
#     def action_dele(self,re, query_set):
#         query_set.delete()
#     action_dele.dec_name = '批量删除'
#     action_list = [action_dele]

class UserConfig(ModelXadmin):
    list_display = ['id','name','username','password','email','depart']
    head_list = ['id', '名字', '用户名', '密码', '邮箱', '部门']
class ClassListConfig(ModelXadmin):
    def display_classname(self, obj):
        class_name = "%s(%s)期"%(obj.course.name, str(obj.semester))
        return class_name

    list_display = [ 'id', 'school', display_classname, 'price',  'teachers', 'tutor']
    head_list = ['id', '学校', '班级名称', '价钱',  '代课老师', '班主任', ]
Xadmin.register(School)
Xadmin.register(UserInfo, UserConfig)
Xadmin.register(School)
Xadmin.register(ClassList, ClassListConfig)

class CustomerConfig(ModelXadmin):

    def display_gender(self, obj):
        return obj.get_gender_display()

    def display_course(self, obj):

        temp =[]

        for cou in obj.course.all():
            str_a = '<a class="btn btn-info" href="/Xadmin/crms9/customer/cancel_course/{}/{}/">{}</a>'.format(obj.pk, cou.pk,cou)
            temp.append(str_a)

        return mark_safe(" ".join(temp))

    def cancel_course(self, re, customer_id, course_id):

        obj = Customer.objects.filter(pk=customer_id).first()
        obj.course.remove(course_id)

        return redirect('/Xadmin/crms9/customer/view/')

    def public_course(self, re):

        import datetime
        now = datetime.datetime.now()
        san_data = datetime.timedelta(days=3)
        shiwu_data = datetime.timedelta(days=15)
        p_list = Customer.objects.filter(Q(recv_date__lt=now-shiwu_data)|Q(last_consult_date__lt=now-san_data)).filter(status=2)

        return  render(re, 'public_customer.html', locals())

    def gen(self, re, pid):
        import datetime
        user_id = 16
        import datetime
        now = datetime.datetime.now()
        san_data = datetime.timedelta(days=3)
        shiwu_data = datetime.timedelta(days=15)
        ret = Customer.objects.filter(Q(recv_date__lt=now-shiwu_data)|Q(last_consult_date__lt=now-san_data)).filter(status=2, pk=pid).update(consultant_id =user_id, recv_date=now, last_consult_date=now,)
        if not ret:
            return HttpResponse('已经被跟进')
        CustomerDistrbute.objects.create(customer_id=pid, consultant_id =user_id, date=now,status=1)
        return HttpResponse('跟进成功')

    def mycustomer(self, re):
        user_id = 16
        ke_list = CustomerDistrbute.objects.filter(consultant=user_id)

        return render(re, 'myke.html', locals())
    def extra_url(self):

        temp = []
        temp.append(re_path('cancel_course/(\d+)/(\d+)/', self.cancel_course))
        temp.append(path('public/', self.public_course))
        temp.append(re_path('gen/(\d+)/', self.gen))
        temp.append(path('mycustomer/', self.mycustomer))

        return temp

    head_list = ['名字', '性别', '咨询课程', '课程顾问']
    list_display = ['name', display_gender, display_course, 'consultant']
Xadmin.register(Customer, CustomerConfig)
Xadmin.register(Department)
Xadmin.register(Course)


class ConsultRecordConfig(ModelXadmin):
    serch_list = ['customer']
    head_list = ['咨询客户', '跟踪人', '跟踪日期', '内容']
    list_display = ['customer', 'consultant', 'date', 'note']

Xadmin.register(ConsultRecord, ConsultRecordConfig)


class StudyRecordConfig(ModelXadmin):

    def action_late(self, re, query_set):
        query_set.update(record='late')

    def lu_cheng(self, re, cou_re_id):
        if re.method == 'POST':

            data = {}
            for key, val in re.POST.items():

                if key == "csrfmiddlewaretoken":
                    continue
                field, pk = key.rsplit('_', 1)

                if pk in data:
                    data[pk][field] = val
                else:
                    data[pk] = {field:val}

                for k,v in data.items():
                    StudyRecord.objects.filter(pk=pk).update(**v)

            return redirect(re.path)
        else:

            st_re = StudyRecord.objects.filter(course_record=cou_re_id)
            scro_cho = StudyRecord.score_choices

        return render(re, 'lu_cheng.html', locals())

    def extra_url(self):
        temp = []
        temp.append(re_path('lu_cheng/(\d+)/', self.lu_cheng))
        return temp
    action_late.dec_name = '批量迟到'
    action_list = [action_late]
    head_list = ['第几天课程', '学生', '上课记录', '成绩记录']
    list_display = ['course_record', 'student', 'record', 'score' ]
    serch_list = ['course_record']
Xadmin.register(StudyRecord, StudyRecordConfig)

from django.http import JsonResponse
class StudentConfig(ModelXadmin):
    def show_score(self, re, spid):
        if re.is_ajax():
            sid = re.GET.get('sid', 0)
            cid = re.GET.get('cid', 0)
            stu_s = StudyRecord.objects.filter(student=sid,course_record__class_obj=cid)
            data = []
            for s in stu_s:
                data.append([
                    'day{}'.format(s.course_record.day_num),
                    s.score
                ])
            return JsonResponse(data, safe=False)

        else:
            stu = Student.objects.filter(pk=spid).first()
            class_list = stu.class_list.all()

        return render(re, 'show_score.html', locals())
    def extra_url(self):
        temp = []
        temp.append(re_path('show_score/(\d+)/',self.show_score))
        return temp

    def display_score(self, obj):
        return mark_safe("<a href='/Xadmin/crms9/student/show_score/{}/'>显示成绩</a>".format(obj.pk))
    list_display = ['customer', 'class_list', display_score]
    head_list = ['姓名', '已报班级', '查看成绩']
Xadmin.register(Student, StudentConfig)


class CourseRecordConfig(ModelXadmin):

    def action_init(self, re, query_set):
        temp = []
        for cour_obj in query_set:
            student_list = Student.objects.filter(class_list__id = cour_obj.class_obj.pk)

            for stu in student_list:
                obj = StudyRecord(student = stu, course_record= cour_obj)
                temp.append(obj)

        StudyRecord.objects.bulk_create(temp)

    def display_score(self, obj):

        return mark_safe("<a href='/Xadmin/crms9/studyrecord/lu_cheng/{}/' >录入成绩</a>".format(obj.pk))
    list_display = ['class_obj', 'day_num', display_score, 'date']
    head_list = ['班级', '天数', '录入成绩', '日期']
    action_init.dec_name = '初始化学习记录'
    action_list = [action_init]
Xadmin.register(CourseRecord, CourseRecordConfig)
