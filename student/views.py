from django.shortcuts import render, redirect
from .forms import NameForm

# Create your views here.
def index(request):
    content = {}
    if request.method == 'POST':
        content = NameForm(request.POST)
        if content.is_valid():
            request.session['form'] = content.cleaned_data
            return redirect('student:home')
    else:
        content['form'] = NameForm()
    return render(request, 'student/index.html', content)

def home(request):
    content = {}
    content['form'] = request.session.get('form')
    if content['form'] and False:
        return render(request, 'student/home.html', content)
    else:
        return redirect('student:index')
