from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserLogin, NewMember
from .models import MyUser

def auth_response(request, content,  key, val):
    user = authenticate(username = key, password = val)
    if user is not None and user.is_active:
        login(request, user)
        if request.user.is_superuser:
            return redirect('app:root_index')
        elif request.user.is_staff:
            return redirect('app:staff_index')
        else:
            return redirect('app:student_index')
    else:
        content['form'].add_error(None, "Invalid mobile or password")
        return render(request, 'index.html', content)

def index(request):
    content = {}
    request.session.clear()
    if request.method == 'POST':
        content['form'] = UserLogin(request.POST)
        if content['form'].is_valid():
            return auth_response(
                request,
                content,
                content['form'].cleaned_data['key'],
                content['form'].cleaned_data['val']
            )
    else:
        content['form'] = UserLogin()
    return render(request, 'index.html', content)


class RootR:
    def index(request):
        content = {}
        if request.user.is_superuser:
            content['student'] = MyUser.objects.get_student()
            content['staff'] = MyUser.objects.get_staff()
            return render(request, 'root/index.html', content)
        else:
            request.session.clear()
            return redirect('app:index')
    
    def newStudent(request):
        content = {}
        if request.user.is_superuser:
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
        if request.user.is_superuser:
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
        if request.user.is_superuser:
            pass
            # content['student'] = MyUser.objects.student(std_id)
        return redirect('app:root_index')
    
    def deleteStudent(request, std_id):
        if request.user.is_superuser:
            MyUser.objects.delete(std_id)
            return redirect('app:root_index')
        else:
            return redirect('app:index')
    
    def editStaff(request, stf_id):
        content = {}
        if request.user.is_superuser:
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
        if request.user.is_authenticated:
            content['student'] = request.user
            return render(request, 'student/index.html', content)
        else:
            request.session.clear()
        return redirect('app:index')


class StaffR:
    def index(request):
        content = {}
        if request.user.is_authenticated and request.user.is_staff:
            content['staff'] = request.user
            return render(request, 'staff/index.html', content)
        else:
            request.session.clear()
            return redirect('app:index')

