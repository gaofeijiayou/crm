from django.shortcuts import render,HttpResponse, redirect
from privilege.models import *
from privilege.service.privilege import initial_session
def login(re):

    if re.method == 'POST':
        username = re.POST.get('user', 0)
        password = re.POST.get('password', 0)

        print(username,password)
        user_obj = User.objects.filter(username=username, password=password).first()
        if user_obj:
            re.session['user_id'] = user_obj.pk
            initial_session(user_obj, re)
            return HttpResponse('343')

    return render(re, 'login.html', locals())
