from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .functions import upload_file_to_blob
from pathlib import Path
from django.contrib import messages
from . import models 
from .forms import UploadFileForm
# Create your views here.

def index(request):
    # if request.method == "POST":
    #     form = UploadFileForm(request.POST)
    #     if form.is_valid:
    #         filename = form.filename()
    #         handle_uploaded_file(request.FILES["file"],filename)
    #         form = UploadFileForm
    #         return render(request,"base.html",{"form":form})
    # # else:
    # form = UploadFileForm
    # return render(request,"index.html",context={"form":form})

    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix
        new_file = upload_file_to_blob(file) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        messages.success(request, f"{file.name} was successfully uploaded")
        form = UploadFileForm()
        return render(request, "index.html", {"form":form}) 
    form = UploadFileForm()
    return render(request, "index.html", {"form":form})

def manage(request):
    files = models.File.objects.filter(deleted=0)
    context = {"files": files}
    return render(request, "manage.html", context=context)
