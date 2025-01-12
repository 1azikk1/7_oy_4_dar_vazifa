from django import forms
from .validators import *
from .models import Course, Student
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'photo']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kurs nomini kiriting',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 1,
                'placeholder': "Kurs haqida ma'lumot kiriting"
            }),

            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

        error_messages = {
            'title': {
                'max_length': "Ko'pi bilan 50 symbol dan iborat matn kiritish mumkin!",
                'unique': "Kurs nomlari har xil bo'lishi kerak!"
            }
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'course']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Talab ismini kiriting'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Talab ismini kiriting'
            }),

            'course': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Talab ismini kiriting'
            })
        }

        error_messages = {
            'email': {
                'unique': "Ushbu email boshqa foydalanuvchi tomonidan foydalanilgan!"
            }
        }


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'form3Example4cg',
        'class': 'form-control form-control-lg'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'form3Example4cdg',
        'class': 'form-control form-control-lg'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={
                'id': 'form3Example1cg',
                'class': 'form-control form-control-lg'
            }),

            'email': forms.EmailInput(attrs={
                'id': 'form3Example3cg',
                'class': 'form-control form-control-lg',
                'required': True
            }),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'typeEmailX-2',
        'class': 'form-control form-control-lg'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'typePasswordX-2',
        'class': 'form-control form-control-lg'
    }))


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=300, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Xabar sarlavhasini kiriting'
    }), label='Sarlavha')
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 1,
        'placeholder': "Xabar matnini kiriting"
    }), label='Xabar')

