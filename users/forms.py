from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'location', 'profile_image']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
   class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستخدم'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تأكيد كلمة المرور'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'password1': 'كلمة المرور',
            'password2': 'تأكيد كلمة المرور',
            'role': 'الدور',
        }


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[('buyer', 'Buyer'), ('seller', 'Seller')],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'phone_number',
            'location',
            'password1',
            'password2',
            'role',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستخدم'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الموقع'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تأكيد كلمة المرور'}),
        }
