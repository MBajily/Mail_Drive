from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from core.views import passwordReset, login_view, CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views

# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('emails/', include('mail.urls')),
    path('drive/', include('drive.urls')),
    path('manager/', include('manager.urls')),
    path('', include('company.urls')),

    # DRF APIs routes
    path('', include('core.urls')),

    path("login", login_view, name="login"),

    # DRF Auth Token
    # path('api/v1/token/request/', obtain_auth_token),

    # Reset Password
    path('api/v1/password/reset/', passwordReset, name="password_reset"),

    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(template_name='reset_password/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', login_view, name="password_reset_complete"),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

