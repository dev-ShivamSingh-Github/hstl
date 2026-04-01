from django import forms
from .models import MyUser
from django.utils.translation import gettext_lazy as _


# Landing page login form
class UserLogin(forms.Form):
    key = forms.CharField(
        label='Mobile',
        max_length=10,
        help_text='Enter your mobile number')
    val = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='Enter your password')

    def clean(self):
        mobile_number = super().clean().get('key')
        if not (
            len(mobile_number) == 10 and
            mobile_number[0] not in "012345" and
            all(c.isdigit() for c in mobile_number)
            ):
            self.add_error('key', 'Enter a valid mobile number')


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

    def clean(self):
        # mobile validation
        input_data = super().clean().get('mobile')
        if not (
            len(input_data) == 10 and
            input_data[0] not in "012345" and
            all(c.isdigit() for c in input_data)
            ):
            self.add_error('mobile', 'Enter a valid mobile number')
        del input_data
        # password validation
        input_data = super().clean().get('password')
        if len(input_data) < 8:
            self.add_error('password', 'The password should have at least 8 characters')
        if not any(c.isupper() for c in input_data):
            self.add_error('password', 'Password should have at least one upper case alphabet')
        if not any(c.islower() for c in input_data):
            self.add_error('password', 'Password should have at least one lower case alphabet')
        if not any(c.isdigit() for c in input_data):
            self.add_error('password', 'Password should contain digit')
        if not any(c in '!@#$%^&*()_=+-/.' for c in input_data):
            self.add_error('password', 'Password should have at least one special symbol: !@#$%^&*()_=+-/.')
        del input_data


class MemberDetail(forms.ModelForm):
    class Meta():
        model = MyUser
        fields = '__all__'
        exclude = ['password', 'is_superuser', 'join_date', 'last_login']
        labels = {
            'name': _('Name'),
            'mobile': _('Mobile'),
            'address': _('Address'),
            'auth_type': _('ID type'),
            'auth_id': _('ID\'s Value'),
            'is_active': _('Is a member?'),
        }
        help_texts = {
            'is_active': _('Uncheck to delete student')
        }

