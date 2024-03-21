from django.urls import path

from . import views

urlpatterns = [
    path("employees", views.employees, name="employees"),
    path("employees/add", views.addEmployee, name="addEmployee"),
    path("employees/<int:employee_id>/deactivate", views.deactivateEmployee, name="deactivateEmployee"),
    path("employees/<int:employee_id>/activate", views.activateEmployee, name="activateEmployee"),
    path("employees/<int:employee_id>/delete", views.deleteEmployee, name="deleteEmployee"),

]
