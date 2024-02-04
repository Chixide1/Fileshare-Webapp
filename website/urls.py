from django.urls import path
from . import views

#urlconf
urlpatterns = [
    path("", views.index, name="index"),
    path("manage/", views.manage, name="manage")
]