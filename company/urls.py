from django.urls import path

from . import views, mail

urlpatterns = [
    path("employees", views.employees, name="employees"),
    path("employees/add", views.addEmployee, name="addEmployee"),
    path("employees/<int:employee_id>/deactivate", views.deactivateEmployee, name="deactivateEmployee"),
    path("employees/<int:employee_id>/activate", views.activateEmployee, name="activateEmployee"),
    path("employees/<int:employee_id>/delete", views.deleteEmployee, name="deleteEmployee"),

    # Mail Routes
    # path("mail", mail.inbox, name="inbox"),
    # path("mail/emails", mail.compose, name="compose"),
    # path("mail/emails/<int:email_id>", mail.email, name="email"),
    # path("mail/emails/<str:mailbox>", mail.mailbox, name="mailbox"),
    # path("mail/emails/search/<str:query>", mail.search, name="search"),

]
