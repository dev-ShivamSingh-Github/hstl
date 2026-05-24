from django import forms
from .models import MyUser, Room
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

