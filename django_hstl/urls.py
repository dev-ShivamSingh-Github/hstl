from django.urls import path
from .views import index, RootR, StudentR, StaffR, logout_view

app_name = 'hstl'
urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout_view, name='logout'),
    
    # Root/Admin Paths
    path('root/', RootR.index, name='root_index'),
    path('root/newStudent/', RootR.newStudent, name='new_student'),
    path('root/infoStudent/<int:std_id>/', RootR.infoStudent, name='info_student'),
    path('root/studentProfile/<int:std_id>/', RootR.studentProfile, name='student_profile'),
    path('root/newStaff/', RootR.newStaff, name='new_staff'),
    path('root/infoStaff/<int:stf_id>/', RootR.infoStaff, name='info_staff'),
    path('root/staffProfile/<int:stf_id>/', RootR.staffProfile, name='staff_profile'),
    path('root/newRoom/', RootR.newRoom, name='new_room'),
    path('root/infoRoom/<int:room_id>/', RootR.infoRoom, name='info_room'),
    path('root/newHostel/', RootR.newHostel, name='new_hostel'),
    path('root/infoHostel/<int:hostel_id>/', RootR.infoHostel, name='info_hostel'),
    path('root/listAllocations/', RootR.listAllocations, name='list_allocations'),
    path('root/newAllocation/', RootR.newAllocation, name='new_allocation'),
    path('root/listInvoices/', RootR.listInvoices, name='list_invoices'),
    path('root/newInvoice/', RootR.newInvoice, name='new_invoice'),
    path('root/newPayment/<int:invoice_id>/', RootR.newPayment, name='new_payment'),

    # Student Paths
    path('student/', StudentR.index, name='student_index'),
    path('student/updateProfile/', StudentR.updateProfile, name='student_update_profile'),
    path('student/myRoom/', StudentR.myRoom, name='student_my_room'),
    path('student/myInvoices/', StudentR.myInvoices, name='student_my_invoices'),
    path('student/complaints/', StudentR.listComplaints, name='student_complaints'),
    path('student/newComplaint/', StudentR.newComplaint, name='student_new_complaint'),
    path('student/leaves/', StudentR.listLeaves, name='student_leaves'),
    path('student/newLeave/', StudentR.newLeave, name='student_new_leave'),

    # Staff Paths
    path('staff/', StaffR.index, name='staff_index'),
    path('staff/updateProfile/', StaffR.updateProfile, name='staff_update_profile'),
    path('staff/viewHostel/', StaffR.viewHostel, name='staff_view_hostel'),
    path('staff/complaints/', StaffR.listComplaints, name='staff_complaints'),
    path('staff/updateComplaint/<int:complaint_id>/', StaffR.updateComplaint, name='staff_update_complaint'),
    path('staff/leaves/', StaffR.listLeaves, name='staff_leaves'),
    path('staff/updateLeave/<int:leave_id>/', StaffR.updateLeave, name='staff_update_leave'),
    path('staff/visitors/', StaffR.listVisitors, name='staff_visitors'),
    path('staff/logVisitor/', StaffR.logVisitor, name='staff_log_visitor'),
]
