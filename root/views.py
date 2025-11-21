from django.shortcuts import render

# Create your views here.
def index(request):
    content = None
    return render(request, 'root/index.html', content)
