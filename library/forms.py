from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from library.models import Code


class BookForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200)
    count = forms.IntegerField(min_value=1)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    change_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        change_password = cleaned_data.get('change_password')
        confirm_password = cleaned_data.get('confirm_password')

        if change_password != confirm_password:
            raise forms.ValidationError('Password do not match!')
        return cleaned_data


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Email Does Not Exist')
        return email

class RestorePassword(forms.Form):
    username = forms.CharField(max_length=255)
    code = forms.CharField(max_length=4)
    code = forms.CharField(max_length=200)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        code = cleaned_data.get('code')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        user = User.objects.filter(username=username).first()

        if not user:
            raise ValidationError('User Not Found')

        if not Code.objects.filter(user=user, code_number=code, expired_data__gt=timezone.now()):
            raise ValidationError(f'Code is incorrect {timezone.now()}')

        if password != re_password:
            raise forms.ValidationError('Password do not match!')

        return cleaned_data

    def update(self):
        user = User.objects.filter(username=self.cleaned_data.get('username')).first()
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        user.save()
