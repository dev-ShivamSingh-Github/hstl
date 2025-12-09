from django import forms
from .models import Student, Staff
from django.utils.translation import gettext_lazy as _


# Landing page login form
class Login(forms.Form):
    key = forms.CharField(label='User Name', max_length=10)
    val = forms.CharField(label='Password', widget=forms.PasswordInput)


class NewStudent(forms.ModelForm):
    class Meta():
        model = Student
        fields = '__all__'
        exclude = ['std_active', 'std_join_date']
        labels = {
            'std_name': _('Name'),
            'std_mobile': _('Mobile'),
            'std_address': _('Address'),
            'std_auth_id': _('ID\'s Value'),
            'std_auth_type': _('ID type'),
        }
        error_messages = {
            'std_mobile':{
                'unique': 'A student already exists with this mobile number.',
            },
            'std_auth_id':{
                'unique': 'A student already exists with this auth id.',
            }
        }
        help_texts = {
            'std_name': _('Full Name of the the student'),
            'std_mobile': _('(+91) 10 digit Mobile number of the student'),
            'std_address': _('Full Address of the student'),
            'std_auth_id': _('Authentic ID number of the student'),
            'std_auth_type': _('Type of the Authentic ID'),
        }


class NewStaff(forms.ModelForm):
    class Meta():
        model = Staff
        fields = '__all__'
        exclude = ['stf_active', 'stf_join_date']
        labels = {
            'stf_name': _('Name'),
            'stf_mobile': _('Mobile'),
            'stf_address': _('Address'),
            'stf_auth_id': _('ID\'s Value'),
            'stf_auth_type': _('ID type'),
        }
        error_messages = {
            'stf_mobile':{
                'unique': 'A staff already exists with this mobile number.',
            },
            'stf_auth_id':{
                'unique': 'A staff already exists with this auth id.',
            }
        }
        help_texts = {
            'stf_name': _('Full Name of the the staff'),
            'stf_mobile': _('(+91) 10 digit Mobile number of the staff'),
            'stf_address': _('Full Address of the staff'),
            'stf_auth_id': _('Authentic ID number of the staff'),
            'stf_auth_type': _('Type of the Authentic ID'),
        }

