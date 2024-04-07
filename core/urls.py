from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )

from . import views

urlpatterns = [
    # path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("drive/", views.files, name="files"),
	path("emails/", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('login/redirect/', views.login_redirect_page, name="login_redirect_page"),
]
