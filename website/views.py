from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .functions import upload_file_to_blob, download_blob, delete_blob
from pathlib import Path
from django.contrib import messages
from . import models 
from .forms import UploadFileForm
import mimetypes
# Create your views here.

def index(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix
        new_file = upload_file_to_blob(file) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        messages.success(request, f"{file.name} was successfully uploaded")

    form = UploadFileForm()
    return render(request, "website/upload.html", {"form":form})

def manage(request):
    files = models.File.objects.filter(deleted=0)
    context = {"files": files}
    return render(request, "website/manage.html", context=context)

def download_file(request, file_id):
    file = models.File.objects.get(pk=file_id)
    file_name = file.file_name
    file_type, _ = mimetypes.guess_type(file_name)
    url = file.file_url
    blob_name = url.split("/")[-1]
    blob_content = download_blob(blob_name)
    if blob_content:
        response = HttpResponse(blob_content.readall(), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        messages.success(request, f"{file_name} was successfully downloaded")
        response = redirect("/manage/")
        return response
    return Http404


def delete_file(request,file_id):
    file = models.File.objects.get(pk=file_id)
    file_name = file.file_name
    delete_blob(file.file_url)
    file.deleted = 1
    file.save()
    messages.success(request, f"{file_name} was successfully downloaded")
    response = redirect("/manage/")
    return response