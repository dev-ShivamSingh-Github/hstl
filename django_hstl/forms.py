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
            'is_active': _('Uncheck to delete student')
        }

