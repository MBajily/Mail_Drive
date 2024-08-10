from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    # path("register", views.register, name="register"),
    path('login/redirect/', views.login_redirect_page, name="login_redirect_page"),

    # API Routes
    path("compose/", views.compose, name="compose"),
    path("email/<int:email_id>", views.email, name="email"),
    path("<str:mailbox>", views.mailbox, name="mailbox"),
    path("search/<str:query>", views.search, name="search"),
]
