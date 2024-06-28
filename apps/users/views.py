from django.shortcuts import render, redirect
from .forms import RegisterForm
from django_htmx.http import HttpResponseClientRedirect
from django.contrib import messages

# Create your views here.
def register(request):
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