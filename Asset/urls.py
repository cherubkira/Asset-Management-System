from django.contrib import admin
from django.urls import path, include
from asset1 import views  # import app views

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    path('', include('asset1.urls', namespace='asset1')),


    # Auth (login/logout/password reset)
    path("accounts/", include("django.contrib.auth.urls")),

    
]

