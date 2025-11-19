from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
   
    path("admin/", admin.site.urls),
    path('', include('asset1.urls', namespace='asset1')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('api/', include('asset1.api.urls')),

    
]


# CRITICAL STEP: Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)