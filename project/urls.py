from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/emails/', include('mail.urls')),
    path('api/v1/drive/', include('drive.urls')),
    path('api/v1/manager/', include('manager.urls')),
    path('api/v1/admin/', include('company.urls')),

    # DRF APIs routes
    path('api/v1/', include('core.urls')),

    # DRF Auth Token
    # path('api/v1/token/request/', obtain_auth_token),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

