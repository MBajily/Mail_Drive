from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )

from . import views, update_profile, otp

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path("get-started/", views.getStartedPage, name="getStarted"),
    # path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("me/profile/update", update_profile.updateProfile, name="myProfile"),
    path("me/password/update", update_profile.updatePassword, name="myPassword"),

    path("password/reset", views.resetPasswordRequest, name="passwordReset"),

    path("drive/", views.files, name="files"),
	path("emails/", views.index, name="index"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.sign_up, name="sign_up"),
    path('login/redirect/', views.login_redirect_page, name="login_redirect_page"),
    path('login/email/otp', otp.emailOTP, name="emailOTP"),
    path('login/phone/otp', otp.smsOTP, name="smsOTP"),
]
