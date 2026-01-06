from django import forms
from .models import MyUser
from django.utils.translation import gettext_lazy as _


# Landing page login form
class Login(forms.Form):
    key = forms.CharField(label='User Name', max_length=10)
    val = forms.CharField(label='Password', widget=forms.PasswordInput)


class NewMember(forms.ModelForm):
    class Meta():
        model = MyUser
        fields = '__all__'
        exclude = ['is_active', 'is_staff', 'join_date', 'last_login']
        labels = {
            'name': _('Name'),
            'mobile': _('Mobile'),
            # 'password': _('Password'),
            'address': _('Address'),
            'auth_type': _('ID type'),
            'auth_id': _('ID\'s Value'),
        }
        error_messages = {
            'mobile':{
                'unique': 'A user already exists with this mobile number.',
            },
            'auth_id':{
                'unique': 'A user already exists with this auth id.',
            }
        }
        help_texts = {
            'name': _('Full Name of the the student'),
            'mobile': _('(+91) 10 digit Mobile number of the student'),
            'address': _('Full Address of the student'),
            'auth_id': _('Authentic ID number of the student'),
            'auth_type': _('Type of the Authentic ID'),
        }

