from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from .functions import upload_file_to_blob, download_blob, delete_blob, bytesto
from pathlib import Path
from django.contrib import messages
from . import models 
from .forms import UploadFileForm
import mimetypes
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

def index(request):
    return redirect("/login/")

@login_required
def upload_files(request):
    files = models.File.objects.filter(user=request.user)
    print(files)
    
    b_used = 0
    for file in files:
        b = file.file_size
        b_used += int(b)
    print(b_used)
    mb_used = bytesto(b_used,'m')
    print(mb_used)

    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        storage_quota = file.size + b_used
        storage_quota = bytesto(storage_quota,'m')
        
        if storage_quota > 100:
            messages.error(request, f"Can't upload {file.name} as it will exceed your storage quota!")
            pass
        ext = Path(file.name).suffix
        new_file = upload_file_to_blob(file) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.user = request.user
        new_file.file_size = file.size
        new_file.save()
        messages.success(request, f"{file.name} was successfully uploaded")
    
    form = UploadFileForm()
    return render(request, "website/upload_files.html", {"form":form,"mb_used":mb_used})

@login_required
def manage_files(request):
    files = models.File.objects.filter(user=request.user)
    context = {"files": files}
    return render(request, "website/manage_files.html", context=context)

@login_required
def download_files(request, file_id):
    file = models.File.objects.get(pk=file_id)
    if file.user == request.user:
        file_name = file.file_name
        file_type, _ = mimetypes.guess_type(file_name)
        url = file.file_url
        blob_name = url.split("/")[-1]
        blob_content = download_blob(blob_name)
        if blob_content:
            response = HttpResponse(blob_content.readall(), content_type=file_type)
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            messages.success(request, f"{file_name} was successfully downloaded")
            return response
        return Http404
    else:
        return HttpResponseForbidden()

@login_required
def delete_files(request,file_id):
    file = models.File.objects.get(pk=file_id)
    if file.user == request.user:
        file_name = file.file_name
        delete_blob(file.file_url)
        file.delete()
        messages.success(request, f"{file_name} was successfully deleted")
        response = redirect("/manage/")
        return response
    else:
        return HttpResponseForbidden()