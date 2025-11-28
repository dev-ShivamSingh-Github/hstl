from django.shortcuts import render, redirect
from .forms import LoginRoot as login
from .forms import NewStudent as newstd

def counter(x):
    if x == 0:
        pass
    else:
        pass

# Create your views here.
def index(request):
    content = {}
    request.session['key'] = None
    request.session['val'] = None
    if request.method == 'POST':
        content['form'] = login(request.POST)
        if content['form'].is_valid():
            request.session['key'] = content['form'].cleaned_data['key']
            request.session['val'] = content['form'].cleaned_data['val']
            # counter(0) #starting the session counter
            return redirect('root:home')
    else:
        content['form'] = login()
    return render(request, 'root/index.html', content)

def home(request):
    content = {}
    if request.session.get('key') == 'Shivam'and request.session.get('val') == 'admin':
        # counter(1) # ending the session
        if request.method == 'POST':
            content['form'] = newstd(request.POST)
            if content['form'].is_valid():
                # print('\n\n\n', content['form'].cleaned_data, '\n\n\n')
                content['form'].save()
        else:
            content['form'] = newstd()
        return render(request, 'root/home.html', content)
    else:
        request.session.clear()
        return redirect('root:index')
