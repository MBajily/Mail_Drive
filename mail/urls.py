from django.urls import path

from . import views

urlpatterns = [
    path("<str:mailbox>", views.getMailbox),
    path("compose/new", views.compose),
    path("email/<str:pk>/", views.getEmail),
    path("email/<str:pk>/update", views.updateEmail),
    path("mailbox/search", views.searchEmail),
]
