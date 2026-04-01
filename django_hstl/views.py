from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserLogin, NewMember, MemberDetail
from .models import MyUser

def auth_response(request, content,  key, val):
    user = authenticate(username = key, password = val)
    if user is not None and user.is_active:
        login(request, user)
        if request.user.is_superuser:
            return redirect('hstl:root_index')
        elif request.user.is_staff:
            return redirect('hstl:staff_index')
        else:
            return redirect('hstl:student_index')
    else:
        content['form'].add_error(None, "Login Error, Invalid Value(s)")
        return render(request, 'index.html', content)

def index(request):
    content = {}
    request.session.aflush()
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
            request.session.flush()
            return redirect('hstl:index')
    
    def newStudent(request):
        content = {}
        if request.user.is_superuser:
            if request.method == 'POST':
                content['form'] = NewMember(request.POST)
                if content['form'].is_valid():
                    # new_id = MyUser.objects.create_student(content['form'].cleaned_data)
                    # return redirect('hstl:info_student', std_id=new_id)
                    return redirect(
                        'hstl:info_student',
                        std_id = MyUser.objects.create_student(content['form'].cleaned_data)
                    )
            else:
                content['form'] = NewMember()
            return render(request, 'root/newStudent.html', content)
        else:
            return redirect('hstl:index')
    
    def newStaff(request):
        content = {}
        if request.user.is_superuser:
            if request.method == 'POST':
                content['form'] = NewMember(request.POST)
                if content['form'].is_valid():
                    # new_id = MyUser.objects.create_staff(content['form'].cleaned_data)
                    # return redirect('hstl:info_staff', stf_id=new_id)
                    return redirect(
                        'hstl:info_staff',
                        stf_id = MyUser.objects.create_staff(content['form'].cleaned_data)
                    )
            else:
                content['form'] = NewMember()
            return render(request, 'root/newStaff.html', content)
        else:
            return redirect('hstl:index')
    
    def infoStudent(request, std_id):
        content = {}
        content['student'] = MyUser.objects.get_student(std_id)
        if request.user.is_superuser and content['student'] is not None:
            if request.method == 'POST':
                content['form'] = MemberDetail(request.POST, instance=content['student'])
                if content['form'].is_valid():
                    content['form'].save()
                    return redirect('hstl:root_index')
            else:
                content['form'] = MemberDetail(instance=content['student'])
            return render(request, 'root/infoStudent.html', content)
        else:
            return redirect('hstl:root_index')
    
    def infoStaff(request, stf_id):
        content = {}
        content['staff'] = MyUser.objects.get_staff(stf_id)
        if request.user.is_superuser and content['staff'] is not None:
            if request.method == 'POST':
                content['form'] = MemberDetail(request.POST, instance=content['staff'])
                if content['form'].is_valid():
                    content['form'].save()
                    return redirect('hstl:root_index')
            else:
                content['form'] = MemberDetail(instance=content['staff'])
            return render(request, 'root/infoStaff.html', content)
        else:
            return redirect('hstl:root_index')


class StudentR:
    def index(request):
        content = {}
        if request.user.is_authenticated:
            content['student'] = request.user
            return render(request, 'student/index.html', content)
        else:
            request.session.flush()
            return redirect('hstl:index')


class StaffR:
    def index(request):
        content = {}
        if request.user.is_authenticated and request.user.is_staff:
            content['staff'] = request.user
            return render(request, 'staff/index.html', content)
        else:
            request.session.flush()
            return redirect('hstl:index')

