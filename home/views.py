from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login

from .forms import SignUpForm


def home(request):
    return render (request,'home/index.html')

def signUp(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request,user)
            return redirect('home')
