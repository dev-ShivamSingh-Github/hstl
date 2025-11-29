from django.shortcuts import render, redirect

def index(request):
    content = {}
    return render(request, 'index.html', content)
