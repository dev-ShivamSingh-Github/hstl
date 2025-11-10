from django.urls import path
from . import views

app_name = 'student'
urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
]

# i can have only one page based web app...
# in form's action the url can be named url 
# {% url 'studindex' %}