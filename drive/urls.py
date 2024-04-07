from django.urls import path

from . import views

urlpatterns = [
    path("<str:drivebox>", views.getDrivebox, name="drivebox"),
    path("files/search", views.search),
    path("file/<int:file_id>", views.updateFile, name="markFile"),
    path("files/upload", views.uploadFile, name="uploadFile"),
]
