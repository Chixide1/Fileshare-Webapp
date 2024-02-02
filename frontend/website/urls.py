from django.urls import path
from . import views

#urlconf
urlpatterns = [
    path("", views.index, name="index"),
]