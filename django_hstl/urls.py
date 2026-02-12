from django.urls import path
from .views import index, RootR, StudentR, StaffR

app_name = 'app'
urlpatterns = [
    path('', index, name='index'),
    path('root/', RootR.index, name='root_index'),
    path('root/newStudent', RootR.newStudent, name='new_student'),
    path('root/newStaff', RootR.newStaff, name='new_staff'),
    path('root/editStudent/<int:std_id>', RootR.editStudent, name='edit_student'),
    path('root/deleteStudent/<int:std_id>', RootR.deleteStudent, name='delete_student'),
    path('root/editStaff/<int:stf_id>', RootR.editStaff, name='edit_staff'),
    path('root/deleteStaff/<int:stf_id>', RootR.deleteStaff, name='delete_staff'),
    path('student/', StudentR.index, name='student_index'),
    path('staff/', StaffR.index, name='staff_index'),
]
