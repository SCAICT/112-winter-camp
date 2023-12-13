from django import forms
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from DataProcess.form import RegisterForm,LoginForm
from django.contrib.auth import authenticate, login

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    form=RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
    redirect('../login')  #重新導向到登入畫面
    context={'form':form}
    return render(request,'../templates/register.html',context)

def login(request):
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, '../templates/login.html', context)

def consent(request):
    return render(request, 'consent.html')

    




