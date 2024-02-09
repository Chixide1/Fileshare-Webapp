from django.urls import path
from . import views

#urlconf
urlpatterns = [
    path("", views.index, name="index"),
    path("upload_files/", views.upload_files, name="upload_files"),
    path("manage_files/", views.manage_files, name="manage_files"),
    path('download_files/<int:file_id>/', views.download_files, name="download_files"),
    path('delete_files/<int:file_id>/', views.delete_files, name="delete_files"),
    path('create_sas/<int:file_id>/', views.create_sas, name="create_sas")
]