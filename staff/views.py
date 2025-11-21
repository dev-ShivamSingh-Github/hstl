from django.shortcuts import render

# Create your views here.
def index(request):
    content = None
    return render(request, 'staff/index.html', content)
