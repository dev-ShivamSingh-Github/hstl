from django.urls import path
from .views import index, RootR, StudentR, StaffR

app_name = 'app'
urlpatterns = [
    path('', index, name='index'),
    path('root/', RootR.index, name='root_index'),
    path('root/newStudent', RootR.newStudent, name='newStudent'),
    path('root/newStaff', RootR.newStaff, name='newStaff'),
    path('root/editStudent/<int:std_id>', RootR.editStudent, name='editStudent'),
    path('root/deleteStudent/<int:std_id>', RootR.deleteStudent, name='deleteStudent'),
    path('root/editStaff/<int:stf_id>', RootR.editStaff, name='editStaff'),
    path('root/deleteStaff/<int:stf_id>', RootR.deleteStaff, name='deleteStaff'),
    path('student/', StudentR.index, name='student_index'),
    path('staff/', StaffR.index, name='staff_index'),
]
