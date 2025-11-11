from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('assets/', views.getAssets),
    path('assets/<int:pk>/', views.getAssets),
]