from django.urls import path

from . import views

urlpatterns = [
    path("<str:mailbox>", views.getMailbox, name="mailbox"),
    path("compose/new", views.compose, name="compose"),
    path("email/<str:pk>/", views.getEmail, name="email"),
    path("email/<str:pk>", views.updateEmail),
    path("mailbox/search", views.searchEmail, name="search"),
]
