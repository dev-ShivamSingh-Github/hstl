from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from .forms import (
    UserLogin, NewMember, MemberDetail, RoomDetail,
    StudentProfileForm, StaffProfileForm, HostelForm, AllocationForm,
    InvoiceForm, PaymentForm, StaffAttendanceForm, PayrollForm,
    ComplaintForm, ComplaintUpdateForm, LeaveRequestForm, LeaveRequestUpdateForm, VisitorForm
)
from .models import (
    MyUser, Room, StudentProfile, StaffProfile, Hostel, Allocation,
    Invoice, Payment, StaffAttendance, Payroll, Complaint, LeaveRequest, Visitor
)

# Custom view-level security decorators
def superuser_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_superuser,
        login_url='hstl:index',
        redirect_field_name=None
    )(view_func)

def staff_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_staff,
        login_url='hstl:index',
        redirect_field_name=None
    )(view_func)

def student_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_active and not u.is_staff and not u.is_superuser,
        login_url='hstl:index',
        redirect_field_name=None
    )(view_func)


def auth_response(request, content, key, val):
    user = authenticate(username=key, password=val)
    if user is not None and user.is_active:
        login(request, user)
        if request.user.is_superuser:
            return redirect('hstl:root_index')
        elif request.user.is_staff:
            return redirect('hstl:staff_index')
        else:
            return redirect('hstl:student_index')
    else:
        content['form'].add_error(None, "Login Error, Invalid Value(s)")
        return render(request, 'index.html', content)


def index(request):
    # If user is already authenticated, redirect them directly to their dashboard
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('hstl:root_index')
        elif request.user.is_staff:
            return redirect('hstl:staff_index')
        else:
            return redirect('hstl:student_index')

    content = {}
    from importlib.metadata import version
    content['version'] = version('django-hstl')
    if request.method == 'POST':
        content['form'] = UserLogin(request.POST)
        if content['form'].is_valid():
            return auth_response(
                request,
                content,
                content['form'].cleaned_data['key'],
                content['form'].cleaned_data['val']
            )
    else:
        content['form'] = UserLogin()
    return render(request, 'index.html', content)


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('hstl:index')


class RootR:
    @superuser_required
    def index(request):
        content = {
            'student': MyUser.objects.get_student(),
            'staff': MyUser.objects.get_staff(),
            'inactive': MyUser.objects.get_inactive(),
            'room': Room.objects.all(),
        }
        return render(request, 'root/index.html', content)

    @superuser_required
    def newStudent(request):
        content = {}
        if request.method == 'POST':
            content['form'] = NewMember(request.POST)
            if content['form'].is_valid():
                std_id = MyUser.objects.create_user(content['form'].cleaned_data)
                return redirect('hstl:student_profile', std_id=std_id)
        else:
            content['form'] = NewMember()
        return render(request, 'root/newStudent.html', content)

    @superuser_required
    def newStaff(request):
        content = {}
        if request.method == 'POST':
            content['form'] = NewMember(request.POST)
            if content['form'].is_valid():
                stf_id = MyUser.objects.create_user(content['form'].cleaned_data, True)
                return redirect('hstl:staff_profile', stf_id=stf_id)
        else:
            content['form'] = NewMember()
        return render(request, 'root/newStaff.html', content)

    @superuser_required
    def infoStudent(request, std_id):
        student = MyUser.objects.get_student(std_id)
        if student is None:
            return redirect('hstl:root_index')
        content = {'student': student}
        if request.method == 'POST':
            content['form'] = MemberDetail(request.POST, instance=student)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = MemberDetail(instance=student)
        return render(request, 'root/infoStudent.html', content)

    @superuser_required
    def infoStaff(request, stf_id):
        staff = MyUser.objects.get_staff(stf_id)
        if staff is None:
            return redirect('hstl:root_index')
        content = {'staff': staff}
        if request.method == 'POST':
            content['form'] = MemberDetail(request.POST, instance=staff)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = MemberDetail(instance=staff)
        return render(request, 'root/infoStaff.html', content)

    @superuser_required
    def newRoom(request):
        content = {}
        if request.method == 'POST':
            content['form'] = RoomDetail(request.POST)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = RoomDetail()
        return render(request, 'root/newRoom.html', content)

    @superuser_required
    def infoRoom(request, room_id):
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return redirect('hstl:root_index')
        content = {'room': room}
        if request.method == 'POST':
            content['form'] = RoomDetail(request.POST, instance=room)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = RoomDetail(instance=room)
        return render(request, 'root/infoRoom.html', content)



    @superuser_required
    def newHostel(request):
        content = {}
        if request.method == 'POST':
            content['form'] = HostelForm(request.POST)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = HostelForm()
        return render(request, 'root/newHostel.html', content)

    @superuser_required
    def infoHostel(request, hostel_id):
        try:
            hostel = Hostel.objects.get(pk=hostel_id)
        except Hostel.DoesNotExist:
            return redirect('hstl:root_index')
        content = {'hostel': hostel}
        if request.method == 'POST':
            content['form'] = HostelForm(request.POST, instance=hostel)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = HostelForm(instance=hostel)
        return render(request, 'root/infoHostel.html', content)

    @superuser_required
    def listAllocations(request):
        content = {'allocations': Allocation.objects.all()}
        return render(request, 'root/listAllocations.html', content)

    @superuser_required
    def newAllocation(request):
        content = {}
        if request.method == 'POST':
            content['form'] = AllocationForm(request.POST)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:list_allocations')
        else:
            content['form'] = AllocationForm()
        return render(request, 'root/newAllocation.html', content)

    @superuser_required
    def listInvoices(request):
        content = {'invoices': Invoice.objects.all()}
        return render(request, 'root/listInvoices.html', content)

    @superuser_required
    def newInvoice(request):
        content = {}
        if request.method == 'POST':
            content['form'] = InvoiceForm(request.POST)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:list_invoices')
        else:
            content['form'] = InvoiceForm()
        return render(request, 'root/newInvoice.html', content)

    @superuser_required
    def newPayment(request, invoice_id):
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            return redirect('hstl:list_invoices')
        content = {'invoice': invoice}
        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                payment = form.save(commit=False)
                payment.invoice = invoice
                payment.received_by = request.user
                payment.save()
                return redirect('hstl:list_invoices')
        else:
            content['form'] = PaymentForm(initial={'invoice': invoice})
        return render(request, 'root/newPayment.html', content)

    @superuser_required
    def studentProfile(request, std_id):
        user = MyUser.objects.get_student(std_id)
        if not user:
            return redirect('hstl:root_index')
        profile, created = StudentProfile.objects.get_or_create(user=user)
        content = {'student': user}
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('hstl:info_student', std_id=std_id)
        else:
            content['form'] = StudentProfileForm(instance=profile)
        return render(request, 'root/studentProfile.html', content)

    @superuser_required
    def staffProfile(request, stf_id):
        user = MyUser.objects.get_staff(stf_id)
        if not user:
            return redirect('hstl:root_index')
        profile, created = StaffProfile.objects.get_or_create(user=user)
        content = {'staff': user}
        if request.method == 'POST':
            form = StaffProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('hstl:info_staff', stf_id=stf_id)
        else:
            content['form'] = StaffProfileForm(instance=profile)
        return render(request, 'root/staffProfile.html', content)



    @superuser_required
    def newHostel(request):
        content = {}
        if request.method == 'POST':
            content['form'] = HostelForm(request.POST)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = HostelForm()
        return render(request, 'root/newHostel.html', content)

    @superuser_required
    def infoHostel(request, hostel_id):
        try:
            hostel = Hostel.objects.get(pk=hostel_id)
        except Hostel.DoesNotExist:
            return redirect('hstl:root_index')
        content = {'hostel': hostel}
        if request.method == 'POST':
            content['form'] = HostelForm(request.POST, instance=hostel)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = HostelForm(instance=hostel)
        return render(request, 'root/infoHostel.html', content)

    @superuser_required
    def listAllocations(request):
        content = {'allocations': Allocation.objects.all()}
        return render(request, 'root/listAllocations.html', content)

    @superuser_required
    def newAllocation(request):
        content = {}
        if request.method == 'POST':
            content['form'] = AllocationForm(request.POST)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:list_allocations')
        else:
            content['form'] = AllocationForm()
        return render(request, 'root/newAllocation.html', content)

    @superuser_required
    def listInvoices(request):
        content = {'invoices': Invoice.objects.all()}
        return render(request, 'root/listInvoices.html', content)

    @superuser_required
    def newInvoice(request):
        content = {}
        if request.method == 'POST':
            content['form'] = InvoiceForm(request.POST)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:list_invoices')
        else:
            content['form'] = InvoiceForm()
        return render(request, 'root/newInvoice.html', content)

    @superuser_required
    def newPayment(request, invoice_id):
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            return redirect('hstl:list_invoices')
        content = {'invoice': invoice}
        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                payment = form.save(commit=False)
                payment.invoice = invoice
                payment.received_by = request.user
                payment.save()
                return redirect('hstl:list_invoices')
        else:
            content['form'] = PaymentForm(initial={'invoice': invoice})
        return render(request, 'root/newPayment.html', content)

    @superuser_required
    def studentProfile(request, std_id):
        user = MyUser.objects.get_student(std_id)
        if not user:
            return redirect('hstl:root_index')
        profile, created = StudentProfile.objects.get_or_create(user=user)
        content = {'student': user}
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('hstl:info_student', std_id=std_id)
        else:
            content['form'] = StudentProfileForm(instance=profile)
        return render(request, 'root/studentProfile.html', content)

    @superuser_required
    def staffProfile(request, stf_id):
        user = MyUser.objects.get_staff(stf_id)
        if not user:
            return redirect('hstl:root_index')
        profile, created = StaffProfile.objects.get_or_create(user=user)
        content = {'staff': user}
        if request.method == 'POST':
            form = StaffProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('hstl:info_staff', stf_id=stf_id)
        else:
            content['form'] = StaffProfileForm(instance=profile)
        return render(request, 'root/staffProfile.html', content)


class StudentR:
    @student_required
    def index(request):
        content = {'student': request.user}
        return render(request, 'student/index.html', content)



    @student_required
    def updateProfile(request):
        profile, created = StudentProfile.objects.get_or_create(user=request.user)
        content = {}
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('hstl:student_index')
        else:
            content['form'] = StudentProfileForm(instance=profile)
        return render(request, 'student/updateProfile.html', content)

    @student_required
    def myRoom(request):
        allocations = Allocation.objects.filter(student=request.user, status='A')
        content = {'allocations': allocations}
        return render(request, 'student/myRoom.html', content)

    @student_required
    def myInvoices(request):
        invoices = Invoice.objects.filter(student=request.user)
        content = {'invoices': invoices}
        return render(request, 'student/myInvoices.html', content)

    @student_required
    def listComplaints(request):
        complaints = Complaint.objects.filter(student=request.user)
        content = {'complaints': complaints}
        return render(request, 'student/listComplaints.html', content)

    @student_required
    def newComplaint(request):
        content = {}
        if request.method == 'POST':
            form = ComplaintForm(request.POST)
            if form.is_valid():
                complaint = form.save(commit=False)
                complaint.student = request.user
                complaint.save()
                return redirect('hstl:student_complaints')
        else:
            content['form'] = ComplaintForm()
        return render(request, 'student/newComplaint.html', content)

    @student_required
    def listLeaves(request):
        leaves = LeaveRequest.objects.filter(student=request.user)
        content = {'leaves': leaves}
        return render(request, 'student/listLeaves.html', content)

    @student_required
    def newLeave(request):
        content = {}
        if request.method == 'POST':
            form = LeaveRequestForm(request.POST)
            if form.is_valid():
                leave = form.save(commit=False)
                leave.student = request.user
                leave.save()
                return redirect('hstl:student_leaves')
        else:
            content['form'] = LeaveRequestForm()
        return render(request, 'student/newLeave.html', content)



    @student_required
    def updateProfile(request):
        profile, created = StudentProfile.objects.get_or_create(user=request.user)
        content = {}
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('hstl:student_index')
        else:
            content['form'] = StudentProfileForm(instance=profile)
        return render(request, 'student/updateProfile.html', content)

    @student_required
    def myRoom(request):
        allocations = Allocation.objects.filter(student=request.user, status='A')
        content = {'allocations': allocations}
        return render(request, 'student/myRoom.html', content)

    @student_required
    def myInvoices(request):
        invoices = Invoice.objects.filter(student=request.user)
        content = {'invoices': invoices}
        return render(request, 'student/myInvoices.html', content)

    @student_required
    def listComplaints(request):
        complaints = Complaint.objects.filter(student=request.user)
        content = {'complaints': complaints}
        return render(request, 'student/listComplaints.html', content)

    @student_required
    def newComplaint(request):
        content = {}
        if request.method == 'POST':
            form = ComplaintForm(request.POST)
            if form.is_valid():
                complaint = form.save(commit=False)
                complaint.student = request.user
                complaint.save()
                return redirect('hstl:student_complaints')
        else:
            content['form'] = ComplaintForm()
        return render(request, 'student/newComplaint.html', content)

    @student_required
    def listLeaves(request):
        leaves = LeaveRequest.objects.filter(student=request.user)
        content = {'leaves': leaves}
        return render(request, 'student/listLeaves.html', content)

    @student_required
    def newLeave(request):
        content = {}
        if request.method == 'POST':
            form = LeaveRequestForm(request.POST)
            if form.is_valid():
                leave = form.save(commit=False)
                leave.student = request.user
                leave.save()
                return redirect('hstl:student_leaves')
        else:
            content['form'] = LeaveRequestForm()
        return render(request, 'student/newLeave.html', content)


class StaffR:
    @staff_required
    def index(request):
        content = {'staff': request.user}
        return render(request, 'staff/index.html', content)


    @staff_required
    def updateProfile(request):
        profile, created = StaffProfile.objects.get_or_create(user=request.user)
        content = {}
        if request.method == 'POST':
            form = StaffProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('hstl:staff_index')
        else:
            content['form'] = StaffProfileForm(instance=profile)
        return render(request, 'staff/updateProfile.html', content)

    @staff_required
    def viewHostel(request):
        try:
            profile = request.user.staff_profile
            hostel = profile.hostel_assigned
        except StaffProfile.DoesNotExist:
            hostel = None
        content = {'hostel': hostel}
        return render(request, 'staff/viewHostel.html', content)

    @staff_required
    def listComplaints(request):
        complaints = Complaint.objects.all()
        content = {'complaints': complaints}
        return render(request, 'staff/listComplaints.html', content)

    @staff_required
    def updateComplaint(request, complaint_id):
        try:
            complaint = Complaint.objects.get(pk=complaint_id)
        except Complaint.DoesNotExist:
            return redirect('hstl:staff_complaints')
        content = {'complaint': complaint}
        if request.method == 'POST':
            form = ComplaintUpdateForm(request.POST, instance=complaint)
            if form.is_valid():
                form.save()
                return redirect('hstl:staff_complaints')
        else:
            content['form'] = ComplaintUpdateForm(instance=complaint)
        return render(request, 'staff/updateComplaint.html', content)

    @staff_required
    def listLeaves(request):
        leaves = LeaveRequest.objects.all()
        content = {'leaves': leaves}
        return render(request, 'staff/listLeaves.html', content)

    @staff_required
    def updateLeave(request, leave_id):
        try:
            leave = LeaveRequest.objects.get(pk=leave_id)
        except LeaveRequest.DoesNotExist:
            return redirect('hstl:staff_leaves')
        content = {'leave': leave}
        if request.method == 'POST':
            form = LeaveRequestUpdateForm(request.POST, instance=leave)
            if form.is_valid():
                form.save()
                return redirect('hstl:staff_leaves')
        else:
            content['form'] = LeaveRequestUpdateForm(instance=leave)
        return render(request, 'staff/updateLeave.html', content)

    @staff_required
    def listVisitors(request):
        visitors = Visitor.objects.all()
        content = {'visitors': visitors}
        return render(request, 'staff/listVisitors.html', content)

    @staff_required
    def logVisitor(request):
        content = {}
        if request.method == 'POST':
            form = VisitorForm(request.POST)
            if form.is_valid():
                visitor = form.save(commit=False)
                visitor.logged_by = request.user
                visitor.save()
                return redirect('hstl:staff_visitors')
        else:
            content['form'] = VisitorForm()
        return render(request, 'staff/logVisitor.html', content)

    @staff_required
    def updateProfile(request):
        profile, created = StaffProfile.objects.get_or_create(user=request.user)
        content = {}
        if request.method == 'POST':
            form = StaffProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('hstl:staff_index')
        else:
            content['form'] = StaffProfileForm(instance=profile)
        return render(request, 'staff/updateProfile.html', content)

    @staff_required
    def viewHostel(request):
        try:
            profile = request.user.staff_profile
            hostel = profile.hostel_assigned
        except StaffProfile.DoesNotExist:
            hostel = None
        content = {'hostel': hostel}
        return render(request, 'staff/viewHostel.html', content)

    @staff_required
    def listComplaints(request):
        complaints = Complaint.objects.all()
        content = {'complaints': complaints}
        return render(request, 'staff/listComplaints.html', content)

    @staff_required
    def updateComplaint(request, complaint_id):
        try:
            complaint = Complaint.objects.get(pk=complaint_id)
        except Complaint.DoesNotExist:
            return redirect('hstl:staff_complaints')
        content = {'complaint': complaint}
        if request.method == 'POST':
            form = ComplaintUpdateForm(request.POST, instance=complaint)
            if form.is_valid():
                form.save()
                return redirect('hstl:staff_complaints')
        else:
            content['form'] = ComplaintUpdateForm(instance=complaint)
        return render(request, 'staff/updateComplaint.html', content)

    @staff_required
    def listLeaves(request):
        leaves = LeaveRequest.objects.all()
        content = {'leaves': leaves}
        return render(request, 'staff/listLeaves.html', content)

    @staff_required
    def updateLeave(request, leave_id):
        try:
            leave = LeaveRequest.objects.get(pk=leave_id)
        except LeaveRequest.DoesNotExist:
            return redirect('hstl:staff_leaves')
        content = {'leave': leave}
        if request.method == 'POST':
            form = LeaveRequestUpdateForm(request.POST, instance=leave)
            if form.is_valid():
                form.save()
                return redirect('hstl:staff_leaves')
        else:
            content['form'] = LeaveRequestUpdateForm(instance=leave)
        return render(request, 'staff/updateLeave.html', content)

    @staff_required
    def listVisitors(request):
        visitors = Visitor.objects.all()
        content = {'visitors': visitors}
        return render(request, 'staff/listVisitors.html', content)

    @staff_required
    def logVisitor(request):
        content = {}
        if request.method == 'POST':
            form = VisitorForm(request.POST)
            if form.is_valid():
                visitor = form.save(commit=False)
                visitor.logged_by = request.user
                visitor.save()
                return redirect('hstl:staff_visitors')
        else:
            content['form'] = VisitorForm()
        return render(request, 'staff/logVisitor.html', content)
