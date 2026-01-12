from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .forms import Login, NewMember
from .models import MyUser

def auth_redirect(request, k, v):
    user = authenticate(username = k, password = v)
    if user is not None:
        request.session['id'] = user.pk
        if user.is_superuser:
            request.session['id'] = True
            return 'app:root_index'
        elif user.is_staff:
            return 'app:staff_index'
        else:
            return 'app:student_index'
    else:
        return 'app:index'

def index(request):
    content = {}
    request.session.clear()
    if request.method == 'POST':
        content['form'] = Login(request.POST)
        if content['form'].is_valid():
            return redirect(auth_redirect(
                request,
                content['form'].cleaned_data['key'],
                content['form'].cleaned_data['val']
            ))
    else:
        content['form'] = Login()
    return render(request, 'index.html', content)


class RootR:
    def index(request):
        content = {}
        if request.session.get('id') is True:
            content['student'] = MyUser.objects.get_student()
            content['staff'] = MyUser.objects.get_staff()
            return render(request, 'root/index.html', content)
        else:
            request.session.clear()
            return redirect('app:index')
    
    def newStudent(request):
        content = {}
        if request.session.get('id') is True:
            if request.method == 'POST':
                content['form'] = NewMember(request.POST)
                if content['form'].is_valid():
                    MyUser.objects.create_student(content['form'].cleaned_data)
                    return redirect('app:new_student')
            else:
                content['form'] = NewMember()
            return render(request, 'root/newStudent.html', content)
        else:
            return redirect('app:index')
    
    def newStaff(request):
        content = {}
        if request.session.get('id') is True:
            if request.method == 'POST':
                content['form'] = NewMember(request.POST)
                if content['form'].is_valid():
                    MyUser.objects.create_staff(content['form'].cleaned_data)
                    return redirect('app:new_staff')
            else:
                content['form'] = NewMember()
            return render(request, 'root/newStaff.html', content)
        else:
            return redirect('app:index')
    
    def editStudent(request, std_id):
        content = {}
        if request.session.get('id') is True:
            pass
            # content['student'] = MyUser.objects.student(std_id)
        return redirect('app:root_index')
    
    def deleteStudent(request, std_id):
        if request.session.get('id') is True:
            MyUser.objects.delete(std_id)
            return redirect('app:root_index')
        else:
            return redirect('app:index')
    
    def editStaff(request, stf_id):
        content = {}
        if request.session.get('id') is True:
            pass
            # content['staff'] = MyUser.objects.staff(stf_id)
        return redirect('app:root_index')
    
    def deleteStaff(request, stf_id):
        if request.session.get('id') is True:
            MyUser.objects.delete(stf_id)
            return redirect('app:root_index')
        else:
            return redirect('app:index')


class StudentR:
    def index(request):
        content = {}
        std_id = request.session.get('id')
        if std_id is not None:
            content['student'] = MyUser.objects.student(std_id)
            return render(request, 'student/index.html', content)
        else:
            request.session.clear()
        return redirect('app:index')


class StaffR:
    def index(request):
        content = {}
        stf_id = request.session.get('id')
        if stf_id is not None:
            content['staff'] = MyUser.objects.staff(stf_id)
            return render(request, 'staff/index.html', content)
        else:
            request.session.clear()
            return redirect('app:index')

