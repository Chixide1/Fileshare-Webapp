from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django_htmx.http import HttpResponseClientRedirect
from django.contrib import messages
from django.contrib.auth import get_user_model

# Create your views here.
def register(request: HttpRequest):
    if request.htmx:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your account was successfully created!")
                return HttpResponseClientRedirect("/")
            else:
                return render(request,"users/_register.html",{"form":form})
        form = RegisterForm()     
        return render(request, 'users/_register.html', {"form":form})
    else:
        return redirect('/')
    
def check_username(request: HttpRequest):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<p style='color: red'>This username already exists<p>")
    elif username == "":
        return HttpResponse("<div style='font-size: 12px; margin-top: .25rem' id='id_username_helptext' class='form-text'>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</div>")
    else:
        return HttpResponse("<p style='color: green'>This username is available<p>")