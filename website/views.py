from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from .utils import upload_file_to_blob, download_blob, delete_blob, generate_sas
from pathlib import Path
from django.contrib import messages
from . import models 
from .forms import UploadFileForm
import mimetypes
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return redirect("/login/")

@login_required(login_url="/login/")
def upload_files(request):
    files = models.File.objects.filter(user=request.user)
    storage_quota = 100000000

    b_used = 0
    for file in files:
        b = file.file_size
        b_used += int(b)

    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        storage_used = file.size + b_used
        
        if storage_used > storage_quota:
            messages.error(request, f"Can't upload {file.name} as it will exceed your storage quota!")
        else:
            ext = Path(file.name).suffix
            new_file = upload_file_to_blob(file) 
            new_file.file_name = file.name
            new_file.file_extention = ext
            new_file.user = request.user
            new_file.file_size = file.size
            new_file.save()
            messages.success(request, f"{file.name} was successfully uploaded")
    
    form = UploadFileForm()
    return render(request, "website/upload_files.html", {"form":form,"b_used":b_used})

@login_required(login_url="/login/")
def manage_files(request):
    files = models.File.objects.filter(user=request.user)
    context = {"files": files}
    return render(request, "website/manage_files.html", context=context)

@login_required(login_url="/login/")
def download_files(request, file_id):
    file = models.File.objects.get(pk=file_id)
    
    if file.user == request.user:
        file_name = file.file_name
        file_name = file_name.replace(",","")
        file_type, _ = mimetypes.guess_type(file_name)
        url = file.file_url
        blob_name = url.split("/")[-1]
        blob_content = download_blob(blob_name)

        if blob_content:
            response = HttpResponse(blob_content.readall(),content_type=file_type)
            response['Content-Disposition'] = f"attachment; filename={file_name}"
            messages.success(request, f"{file_name} was successfully downloaded")
            return response
        else:
            messages.error(request, f"{file_name} has expired and been deleted as it's been 2 days since it was uploaded!")
            file.delete()
            return redirect("/manage_files/")
    else:
        return HttpResponseForbidden()

@login_required(login_url="/login/")
def delete_files(request,file_id):
    file = models.File.objects.get(pk=file_id)
    
    if file.user == request.user:
        file_name = file.file_name
        url = file.file_url
        blob_name = url.split("/")[-1]
        msg = delete_blob(blob_name)
        file.delete()
        messages.success(request,file_name + msg)
        return redirect("/manage_files/")
    else:
        return HttpResponseForbidden()
    
@login_required(login_url="/login/")   
def create_sas(request,file_id):
    file = models.File.objects.get(pk=file_id)

    if file.user == request.user:
        file_name = file.file_name
        url = file.file_url
        blob_name = url.split("/")[-1]
        sas = generate_sas(blob_name)

        if sas:
            messages.info(request,f"Here's the share link, it expires in 1 day: {sas}")
            return redirect("/manage_files/")
        else:
            messages.error(request, f"{file_name} has expired and been deleted as it's been 2 days since it was uploaded!")
            file.delete()
            return redirect("/manage_files/")
    else:
        return HttpResponseForbidden()