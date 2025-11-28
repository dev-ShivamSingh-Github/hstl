from django.shortcuts import render, redirect
from .forms import LoginStudent as login

# Create your views here.
def index(request):
    content = {}
    request.session['key'] = None
    request.session['val'] = None
    if request.method == 'POST':
        content = login(request.POST)
        if content.is_valid():
            request.session['key'] = content.cleaned_data['key']
            request.session['val'] = content.cleaned_data['val']
            return redirect('student:home')
    else:
        content['form'] = login()
    return render(request, 'student/index.html', content)

def home(request):
    content = {}
    content['key'] = request.session.get('key')
    content['val'] = request.session.get('val')
    if content['key'] == 'Shivam' and content['val'] == 'admin':
        return render(request, 'student/home.html', content)
    else:
        request.session.clear()
        return redirect('student:index')
