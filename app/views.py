from django.shortcuts import render, redirect
from .forms import Login, NewStudent, NewStaff
from .models import Student, Staff

def auth_redirect(k, v):
    if k == 'root' and v == 'root':
        return 'app:root_index'
    elif k == 'staff' and v == 'staff':
        return 'app:staff_index'
    elif k == 'student' and v == 'student':
        return 'app:student_index'
    else:
        return 'app:index'

def index(request):
    content = {}
    request.session.clear()
    if request.method == 'POST':
        content['form'] = Login(request.POST)
        if content['form'].is_valid():
            request.session['key'] = content['form'].cleaned_data['key']
            request.session['val'] = content['form'].cleaned_data['val']
            return redirect(auth_redirect(request.session['key'], request.session['val']))
    else:
        content['form'] = Login()
    return render(request, 'index.html', content)


class RootR:
    def index(request):
        content = {}
        if request.session.get('key') == 'root'and request.session.get('val') == 'root':
            content['student'] = Student.objects.filter(std_active=True)
            content['staff'] = Staff.objects.filter(stf_active=True)
            return render(request, 'root/index.html', content)
        else:
            request.session.clear()
            return redirect('app:index')
    
    def newStudent(request):
        content = {}
        if request.session.get('key') == 'root'and request.session.get('val') == 'root':
            if request.method == 'POST':
                content['form'] = NewStudent(request.POST)
                if content['form'].is_valid():
                    content['form'].save()
            else:
                content['form'] = NewStudent()
            return render(request, 'root/newStudent.html', content)
        else:
            request.session.clear()
            return redirect('app:index')
    
    def newStaff(request):
        content = {}
        if request.session.get('key') == 'root'and request.session.get('val') == 'root':
            if request.method == 'POST':
                content['form'] = NewStaff(request.POST)
                if content['form'].is_valid():
                    content['form'].save()
            else:
                content['form'] = NewStaff()
            return render(request, 'root/newStaff.html', content)
        else:
            request.session.clear()
            return redirect('app:index')
    
    def editStudent(request, std_id):
        return redirect('app:root_index')
    
    def deleteStudent(request, std_id):
        if request.session.get('key') == 'root'and request.session.get('val') == 'root':
            Student.objects.filter(id=std_id).update(std_active = False)
            return redirect('app:root_index')
        else:
            request.session.clear()
            return redirect('app:index')
    
    def editStaff(request, stf_id):
        return redirect('app:root_index')
    
    def deleteStaff(request, stf_id):
        if request.session.get('key') == 'root'and request.session.get('val') == 'root':
            Staff.objects.filter(id=stf_id).update(stf_active = False)
            return redirect('app:root_index')
        else:
            request.session.clear()
            return redirect('app:index')


class StudentR:
    def index(request):
        content = {}
        if request.session.get('key') == 'student'and request.session.get('val') == 'student':
            return render(request, 'student/index.html', content)
        else:
            request.session.clear()
        return redirect('app:index')


class StaffR:
    def index(request):
        content = {}
        if request.session.get('key') == 'staff'and request.session.get('val') == 'staff':
            return render(request, 'staff/index.html', content)
        else:
            request.session.clear()
            return redirect('app:index')

