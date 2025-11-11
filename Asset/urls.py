from django.contrib import admin
from django.urls import path, include



urlpatterns = [
   
    path("admin/", admin.site.urls),
    path('', include('asset1.urls', namespace='asset1')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('api/', include('asset1.api.urls')),

    
]

