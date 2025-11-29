from django.shortcuts import render, redirect
from .forms import Login

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
            print(content['form'].cleaned_data)
            return redirect(auth_redirect(request.session['key'], request.session['val']))
    else:
        content['form'] = Login()
    return render(request, 'index.html', content)


class RootR:
    def index(request):
        content = {}
        if request.session.get('key') == 'root'and request.session.get('val') == 'root':
            return render(request, 'root/index.html', content)
        else:
            request.session.clear()
            return redirect('app:index')
    
    def hmm(request):
        pass


class StudentR:
    def index(request):
        content = {}
        if request.session.get('key') == 'student'and request.session.get('val') == 'student':
            return render(request, 'student/index.html', content)
        else:
            request.session.clear()
        return redirect('app:index')
    
    def hmm(request):
        pass


class StaffR:
    def index(request):
        content = {}
        if request.session.get('key') == 'staff'and request.session.get('val') == 'staff':
            return render(request, 'staff/index.html', content)
        else:
            request.session.clear()
            return redirect('app:index')
    
    def hmm(request):
        pass

