from django.urls import path
from .views import index, RootR, StudentR, StaffR, logout_view

app_name = 'hstl'
urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout_view, name='logout'),
    
    # Root/Admin Paths
    path('root/', RootR.Index.as_view(), name='root_index'),
    path('root/newStudent/', RootR.NewStudent.as_view(), name='new_student'),
    path('root/infoStudent/<int:std_id>/', RootR.InfoStudent.as_view(), name='info_student'),
    path('root/studentProfile/<int:std_id>/', RootR.StudentProfileView.as_view(), name='student_profile'),
    path('root/newStaff/', RootR.NewStaff.as_view(), name='new_staff'),
    path('root/infoStaff/<int:stf_id>/', RootR.InfoStaff.as_view(), name='info_staff'),
    path('root/staffProfile/<int:stf_id>/', RootR.StaffProfileView.as_view(), name='staff_profile'),
    path('root/newRoom/', RootR.NewRoom.as_view(), name='new_room'),
    path('root/infoRoom/<int:room_id>/', RootR.InfoRoom.as_view(), name='info_room'),
    path('root/newHostel/', RootR.NewHostel.as_view(), name='new_hostel'),
    path('root/infoHostel/<int:hostel_id>/', RootR.InfoHostel.as_view(), name='info_hostel'),
    path('root/listAllocations/', RootR.ListAllocations.as_view(), name='list_allocations'),
    path('root/newAllocation/', RootR.NewAllocation.as_view(), name='new_allocation'),
    path('root/listInvoices/', RootR.ListInvoices.as_view(), name='list_invoices'),
    path('root/newInvoice/', RootR.NewInvoice.as_view(), name='new_invoice'),
    path('root/newPayment/<int:invoice_id>/', RootR.NewPayment.as_view(), name='new_payment'),

    # Student Paths
    path('student/', StudentR.Index.as_view(), name='student_index'),
    path('student/updateProfile/', StudentR.UpdateProfile.as_view(), name='student_update_profile'),
    path('student/myRoom/', StudentR.MyRoom.as_view(), name='student_my_room'),
    path('student/myInvoices/', StudentR.MyInvoices.as_view(), name='student_my_invoices'),
    path('student/complaints/', StudentR.ListComplaints.as_view(), name='student_complaints'),
    path('student/newComplaint/', StudentR.NewComplaint.as_view(), name='student_new_complaint'),
    path('student/leaves/', StudentR.ListLeaves.as_view(), name='student_leaves'),
    path('student/newLeave/', StudentR.NewLeave.as_view(), name='student_new_leave'),

    # Staff Paths
    path('staff/', StaffR.Index.as_view(), name='staff_index'),
    path('staff/updateProfile/', StaffR.UpdateProfile.as_view(), name='staff_update_profile'),
    path('staff/viewHostel/', StaffR.ViewHostel.as_view(), name='staff_view_hostel'),
    path('staff/complaints/', StaffR.ListComplaints.as_view(), name='staff_complaints'),
    path('staff/updateComplaint/<int:complaint_id>/', StaffR.UpdateComplaint.as_view(), name='staff_update_complaint'),
    path('staff/leaves/', StaffR.ListLeaves.as_view(), name='staff_leaves'),
    path('staff/updateLeave/<int:leave_id>/', StaffR.UpdateLeave.as_view(), name='staff_update_leave'),
    path('staff/visitors/', StaffR.ListVisitors.as_view(), name='staff_visitors'),
    path('staff/logVisitor/', StaffR.LogVisitor.as_view(), name='staff_log_visitor'),
]
