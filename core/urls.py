from django.urls import path

from . import views

urlpatterns = [
    path("emails/<str:mailbox>", views.getMailbox),
    path("emails/email/create", views.createEmail),
    path("emails/email/<str:pk>/", views.getEmail),
    path("emails/email/<str:pk>/update", views.updateEmail),
]
