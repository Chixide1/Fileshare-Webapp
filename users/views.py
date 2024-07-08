from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
# Create your views here.

def create_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            return render(request,"users/create_user.html",{"form":form})
    form = RegisterForm()
    return render(request, "users/create_user.html", {"form":form})