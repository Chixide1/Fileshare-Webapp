from django.urls import path
from . import views

#urlconf
urlpatterns = [
    path("", views.index, name="index"),
    path("manage/", views.manage, name="manage_files"),
    path('download_file/<int:file_id>/', views.download_file, name="download_file"),
    path('delete_file/<int:file_id>/', views.delete_file, name="delete_file"),
]