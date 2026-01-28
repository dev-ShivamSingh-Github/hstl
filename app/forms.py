from django import forms
from .models import MyUser
from django.utils.translation import gettext_lazy as _


# Landing page login form
class UserLogin(forms.Form):
    key = forms.CharField(label='Mobile', max_length=10)
    val = forms.CharField(label='Password', widget=forms.PasswordInput)


class NewMember(forms.ModelForm):
    class Meta():
        model = MyUser
        fields = '__all__'
        exclude = ['is_active', 'is_staff', 'is_superuser', 'join_date', 'last_login']
        labels = {
            'name': _('Name'),
            'mobile': _('Mobile'),
            'address': _('Address'),
            'auth_type': _('ID type'),
            'auth_id': _('ID\'s Value'),
            'password': _('Create Password'),
        }
        error_messages = {
            'mobile':{
                'unique': 'A user already exists with this mobile number.',
            },
            'auth_id':{
                'unique': 'A user already exists with this auth id.',
            }
        }

