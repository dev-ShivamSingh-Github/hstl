from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404

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


# --- MIXINS ---
class SuperuserRequiredMixin(UserPassesTestMixin):
    login_url = 'hstl:index'
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

class StaffRequiredMixin(UserPassesTestMixin):
    login_url = 'hstl:index'
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_active and self.request.user.is_staff

class StudentRequiredMixin(UserPassesTestMixin):
    login_url = 'hstl:index'
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_active and not self.request.user.is_staff and not self.request.user.is_superuser


# --- BASE VIEWS ---
class RootBaseView(SuperuserRequiredMixin):
    pass

class StaffBaseView(StaffRequiredMixin):
    pass

class StudentBaseView(StudentRequiredMixin):
    pass


# --- ROOT VIEWS ---
class RootR:
    class Index(RootBaseView, TemplateView):
        template_name = 'root/index.html'
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['student'] = MyUser.objects.get_student()
            context['staff'] = MyUser.objects.get_staff()
            context['inactive'] = MyUser.objects.get_inactive()
            context['room'] = Room.objects.all()
            context['hostel'] = Hostel.objects.all()
            context['allocations'] = Allocation.objects.all()
            context['invoices'] = Invoice.objects.all()
            context['complaints'] = Complaint.objects.all()
            context['stats'] = {
                'total_students': context['student'].count(),
                'total_staff': context['staff'].count(),
                'total_hostels': context['hostel'].count(),
                'total_rooms': context['room'].count(),
                'active_allocations': context['allocations'].filter(status='A').count(),
                'unpaid_invoices': context['invoices'].filter(status='U').count(),
                'pending_complaints': context['complaints'].filter(status='O').count(),
            }
            return context

    class NewStudent(RootBaseView, FormView):
        template_name = 'root/newStudent.html'
        form_class = NewMember
        def form_valid(self, form):
            std_id = MyUser.objects.create_user(form.cleaned_data)
            return redirect('hstl:student_profile', std_id=std_id)

    class NewStaff(RootBaseView, FormView):
        template_name = 'root/newStaff.html'
        form_class = NewMember
        def form_valid(self, form):
            stf_id = MyUser.objects.create_user(form.cleaned_data, True)
            return redirect('hstl:staff_profile', stf_id=stf_id)

    class InfoStudent(RootBaseView, UpdateView):
        model = MyUser
        form_class = MemberDetail
        template_name = 'root/infoStudent.html'
        pk_url_kwarg = 'std_id'
        success_url = reverse_lazy('hstl:root_index')
        def get_object(self, queryset=None):
            obj = MyUser.objects.get_student(self.kwargs.get(self.pk_url_kwarg))
            if not obj:
                raise Http404
            return obj

    class InfoStaff(RootBaseView, UpdateView):
        model = MyUser
        form_class = MemberDetail
        template_name = 'root/infoStaff.html'
        pk_url_kwarg = 'stf_id'
        success_url = reverse_lazy('hstl:root_index')
        def get_object(self, queryset=None):
            obj = MyUser.objects.get_staff(self.kwargs.get(self.pk_url_kwarg))
            if not obj:
                raise Http404
            return obj

    class NewRoom(RootBaseView, CreateView):
        model = Room
        form_class = RoomDetail
        template_name = 'root/newRoom.html'
        success_url = reverse_lazy('hstl:root_index')

    class InfoRoom(RootBaseView, UpdateView):
        model = Room
        form_class = RoomDetail
        template_name = 'root/infoRoom.html'
        pk_url_kwarg = 'room_id'
        success_url = reverse_lazy('hstl:root_index')

    class NewHostel(RootBaseView, CreateView):
        model = Hostel
        form_class = HostelForm
        template_name = 'root/newHostel.html'
        success_url = reverse_lazy('hstl:root_index')

    class InfoHostel(RootBaseView, UpdateView):
        model = Hostel
        form_class = HostelForm
        template_name = 'root/infoHostel.html'
        pk_url_kwarg = 'hostel_id'
        success_url = reverse_lazy('hstl:root_index')

    class ListAllocations(RootBaseView, ListView):
        model = Allocation
        template_name = 'root/listAllocations.html'
        context_object_name = 'allocations'

    class NewAllocation(RootBaseView, CreateView):
        model = Allocation
        form_class = AllocationForm
        template_name = 'root/newAllocation.html'
        success_url = reverse_lazy('hstl:list_allocations')

    class ListInvoices(RootBaseView, ListView):
        model = Invoice
        template_name = 'root/listInvoices.html'
        context_object_name = 'invoices'

    class NewInvoice(RootBaseView, CreateView):
        model = Invoice
        form_class = InvoiceForm
        template_name = 'root/newInvoice.html'
        success_url = reverse_lazy('hstl:list_invoices')

    class NewPayment(RootBaseView, CreateView):
        model = Payment
        form_class = PaymentForm
        template_name = 'root/newPayment.html'
        success_url = reverse_lazy('hstl:list_invoices')

        def get_initial(self):
            initial = super().get_initial()
            invoice = get_object_or_404(Invoice, pk=self.kwargs.get('invoice_id'))
            initial['invoice'] = invoice
            return initial

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['invoice'] = get_object_or_404(Invoice, pk=self.kwargs.get('invoice_id'))
            return context

        def form_valid(self, form):
            payment = form.save(commit=False)
            payment.invoice = get_object_or_404(Invoice, pk=self.kwargs.get('invoice_id'))
            payment.received_by = self.request.user
            payment.save()
            return redirect(self.success_url)

    class StudentProfileView(RootBaseView, UpdateView):
        model = StudentProfile
        form_class = StudentProfileForm
        template_name = 'root/studentProfile.html'
        
        def get_object(self, queryset=None):
            user = get_object_or_404(MyUser, pk=self.kwargs.get('std_id'), is_staff=False, is_superuser=False)
            profile, created = StudentProfile.objects.get_or_create(user=user)
            return profile

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['student'] = get_object_or_404(MyUser, pk=self.kwargs.get('std_id'), is_staff=False, is_superuser=False)
            return context

        def get_success_url(self):
            return reverse_lazy('hstl:info_student', kwargs={'std_id': self.kwargs.get('std_id')})

    class StaffProfileView(RootBaseView, UpdateView):
        model = StaffProfile
        form_class = StaffProfileForm
        template_name = 'root/staffProfile.html'
        
        def get_object(self, queryset=None):
            user = get_object_or_404(MyUser, pk=self.kwargs.get('stf_id'), is_staff=True, is_superuser=False)
            profile, created = StaffProfile.objects.get_or_create(user=user)
            return profile

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['staff'] = get_object_or_404(MyUser, pk=self.kwargs.get('stf_id'), is_staff=True, is_superuser=False)
            return context

        def get_success_url(self):
            return reverse_lazy('hstl:info_staff', kwargs={'stf_id': self.kwargs.get('stf_id')})


# --- STUDENT VIEWS ---
class StudentR:
    class Index(StudentBaseView, TemplateView):
        template_name = 'student/index.html'
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['student'] = self.request.user
            return context

    class UpdateProfile(StudentBaseView, UpdateView):
        model = StudentProfile
        form_class = StudentProfileForm
        template_name = 'student/updateProfile.html'
        success_url = reverse_lazy('hstl:student_index')
        def get_object(self, queryset=None):
            profile, created = StudentProfile.objects.get_or_create(user=self.request.user)
            return profile

    class MyRoom(StudentBaseView, ListView):
        template_name = 'student/myRoom.html'
        context_object_name = 'allocations'
        def get_queryset(self):
            return Allocation.objects.filter(student=self.request.user, status='A')

    class MyInvoices(StudentBaseView, ListView):
        template_name = 'student/myInvoices.html'
        context_object_name = 'invoices'
        def get_queryset(self):
            return Invoice.objects.filter(student=self.request.user)

    class ListComplaints(StudentBaseView, ListView):
        template_name = 'student/listComplaints.html'
        context_object_name = 'complaints'
        def get_queryset(self):
            return Complaint.objects.filter(student=self.request.user)

    class NewComplaint(StudentBaseView, CreateView):
        model = Complaint
        form_class = ComplaintForm
        template_name = 'student/newComplaint.html'
        success_url = reverse_lazy('hstl:student_complaints')
        def form_valid(self, form):
            complaint = form.save(commit=False)
            complaint.student = self.request.user
            complaint.save()
            return redirect(self.success_url)

    class ListLeaves(StudentBaseView, ListView):
        template_name = 'student/listLeaves.html'
        context_object_name = 'leaves'
        def get_queryset(self):
            return LeaveRequest.objects.filter(student=self.request.user)

    class NewLeave(StudentBaseView, CreateView):
        model = LeaveRequest
        form_class = LeaveRequestForm
        template_name = 'student/newLeave.html'
        success_url = reverse_lazy('hstl:student_leaves')
        def form_valid(self, form):
            leave = form.save(commit=False)
            leave.student = self.request.user
            leave.save()
            return redirect(self.success_url)


# --- STAFF VIEWS ---
class StaffR:
    class Index(StaffBaseView, TemplateView):
        template_name = 'staff/index.html'
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['staff'] = self.request.user
            return context

    class UpdateProfile(StaffBaseView, UpdateView):
        model = StaffProfile
        form_class = StaffProfileForm
        template_name = 'staff/updateProfile.html'
        success_url = reverse_lazy('hstl:staff_index')
        def get_object(self, queryset=None):
            profile, created = StaffProfile.objects.get_or_create(user=self.request.user)
            return profile

    class ViewHostel(StaffBaseView, TemplateView):
        template_name = 'staff/viewHostel.html'
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            try:
                profile = self.request.user.staff_profile
                context['hostel'] = profile.hostel_assigned
            except StaffProfile.DoesNotExist:
                context['hostel'] = None
            return context

    class ListComplaints(StaffBaseView, ListView):
        model = Complaint
        template_name = 'staff/listComplaints.html'
        context_object_name = 'complaints'

    class UpdateComplaint(StaffBaseView, UpdateView):
        model = Complaint
        form_class = ComplaintUpdateForm
        template_name = 'staff/updateComplaint.html'
        pk_url_kwarg = 'complaint_id'
        success_url = reverse_lazy('hstl:staff_complaints')

    class ListLeaves(StaffBaseView, ListView):
        model = LeaveRequest
        template_name = 'staff/listLeaves.html'
        context_object_name = 'leaves'

    class UpdateLeave(StaffBaseView, UpdateView):
        model = LeaveRequest
        form_class = LeaveRequestUpdateForm
        template_name = 'staff/updateLeave.html'
        pk_url_kwarg = 'leave_id'
        success_url = reverse_lazy('hstl:staff_leaves')

    class ListVisitors(StaffBaseView, ListView):
        model = Visitor
        template_name = 'staff/listVisitors.html'
        context_object_name = 'visitors'

    class LogVisitor(StaffBaseView, CreateView):
        model = Visitor
        form_class = VisitorForm
        template_name = 'staff/logVisitor.html'
        success_url = reverse_lazy('hstl:staff_visitors')
        def form_valid(self, form):
            visitor = form.save(commit=False)
            visitor.logged_by = self.request.user
            visitor.save()
            return redirect(self.success_url)
