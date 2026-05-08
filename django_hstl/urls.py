from django.urls import path
from .views import index, RootR, StudentR, StaffR

app_name = 'hstl'
urlpatterns = [
    path('', index, name='index'),
    path('root/', RootR.index, name='root_index'),
    path('root/newStudent/', RootR.newStudent, name='new_student'),
    path('root/infoStudent/<int:std_id>', RootR.infoStudent, name='info_student'),
    path('root/newStaff/', RootR.newStaff, name='new_staff'),
    path('root/infoStaff/<int:stf_id>', RootR.infoStaff, name='info_staff'),
    path('student/', StudentR.index, name='student_index'),
    path('staff/', StaffR.index, name='staff_index'),
]
