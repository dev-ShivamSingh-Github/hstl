from django.urls import path
from .views import index, RootR, StudentR, StaffR

app_name = 'app'
urlpatterns = [
    path('', index, name='index'),
    path('root/', RootR.index, name='root_index'),
    path('student/', StudentR.index, name='student_index'),
    path('staff/', StaffR.index, name='staff_index'),
]
