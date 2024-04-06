from django.urls import path

from . import views

urlpatterns = [
    path("drive", views.files, name="files"),
	path("emails", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('login/redirect/', views.login_redirect_page, name="login_redirect_page"),
]
