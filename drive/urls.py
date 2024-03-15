from django.urls import path

from . import views

urlpatterns = [
    path("", views.files, name="files"),
    path("<str:drivebox>", views.drivebox, name="drivebox"),
    path("search/<str:query>", views.search, name="search"),
    path("<int:file_id>", views.markFile, name="markFile"),

]
