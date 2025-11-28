from django import forms


class LoginStudent(forms.Form):
    key = forms.CharField(label='User Name', max_length=10)
    val = forms.CharField(label='Password', widget=forms.PasswordInput)