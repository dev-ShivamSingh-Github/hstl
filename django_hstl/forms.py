from django import forms
from .models import (
    MyUser, Room, StudentProfile, StaffProfile, Hostel, Allocation, 
    Invoice, Payment, StaffAttendance, Payroll, Complaint, LeaveRequest, Visitor
)
from .valids import validate_mobile, validate_password

# Landing page login form
class UserLogin(forms.Form):
    key = forms.CharField(
        label='Mobile',
        max_length=10,
        help_text='Enter your mobile number',
        validators=[validate_mobile]
    )
    val = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='Enter your password',
        # validators=[validate_password]
    )


class NewMember(forms.ModelForm):
    class Meta():
        model = MyUser
        fields = '__all__'
        exclude = ['is_active', 'is_staff', 'is_superuser', 'join_date', 'last_login']
        error_messages = {
            'mobile':{
                'unique': 'A user already exists with this mobile number.',
            },
            'auth_id':{
                'unique': 'A user already exists with this auth id.',
            }
        }

    def clean(self):
        try:
            input_data = super().clean().get('password')
            validate_password(input_data)
        except Exception as e:
            self.add_error(e.code, e)


class MemberDetail(forms.ModelForm):
    class Meta():
        model = MyUser
        fields = '__all__'
        exclude = ['password', 'is_superuser', 'join_date', 'last_login']
        help_texts = {
            'is_active': 'Uncheck to delete student'
        }


class RoomDetail(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['user']

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        exclude = ['user']

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = '__all__'

class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = '__all__'

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

class StaffAttendanceForm(forms.ModelForm):
    class Meta:
        model = StaffAttendance
        fields = '__all__'

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = '__all__'

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        exclude = ['student', 'status', 'assigned_to', 'admin_remarks']

class ComplaintUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status', 'assigned_to', 'admin_remarks']

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        exclude = ['student', 'status', 'approved_by']
        widgets = {
            'departure_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'return_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class LeaveRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status', 'approved_by']

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        exclude = ['logged_by', 'check_out']
        widgets = {
            'check_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


