from django.urls import path

from . import views

urlpatterns = [
    path("<str:drivebox>", views.getDrivebox),
    path("files/search", views.search),
    path("file/<int:file_id>/update", views.updateFile),
    path("files/upload", views.uploadFile),
]
