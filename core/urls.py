from django.urls import path

from . import views

urlpatterns = [
    path("emails/<str:mailbox>", views.getMailbox),
]
