from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="姓名",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    school = forms.CharField(
        label="學校",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    department = forms.CharField(
        label="科別",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    club = forms.CharField(
        label="社團",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label="個人聯絡電話",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    sex = forms.ChoiceField(
        label="生理性別",
        choices=[(1,'男'),(2,'女')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    NationalID=forms.CharField(
        label="身分證字號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    birthday=forms.DateField(
        label="出生年月日",
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    inCaseOfEmergence=forms.CharField(
        label="緊急聯絡人",
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    inCaseOfEmergenceRela=forms.CharField(
        label="緊急聯絡人關係",
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    inCaseOfEmergenceNum=forms.CharField(
        label="緊急聯絡人電話",
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    clothSize = forms.ChoiceField(
        label="衣服尺寸",
        choices=[(1,'XS'),(2,'S'),(3,'M'),(4,'L'),(5,'XL'),(6,'XXL')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    diet=forms.ChoiceField(
        label="飲食",
        choices=[(1,'葷'),(2,'素')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    specialDietNeed=forms.CharField(
        label="特殊飲食習慣",
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    specialDisease=forms.ChoiceField(
        label="是否有特殊疾病",
        choices=[(1,'是'),(2,'否')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    accommodation=forms.ChoiceField(
        label="是否參與住宿",
        choices=[(1,'是'),(2,'否')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    discount=forms.CharField(
        label="團報優惠碼",
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )

class LoginForm(forms.Form):
    emailOrPhone = forms.CharField(
        label="Email/電話",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')