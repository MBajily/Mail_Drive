from django.urls import path

from . import views

urlpatterns = [
    path("", views.files, name="files"),
    path("<str:drivebox>", views.drivebox, name="drivebox"),
]
