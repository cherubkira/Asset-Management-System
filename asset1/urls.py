from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "asset1"

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assets/', views.asset_list, name='asset_list'),
    path('create/', views.asset_create, name='asset-create'),
    path('assets/history/', views.asset_history, name='asset-history'),
    path('assets/category/', views.asset_category, name='asset-category'),
    path('assets/subcategory/', views.asset_subcategory, name='asset-subcategory'),
    path('assets/status/', views.asset_status, name='asset-status'),
    path('assets/comment/', views.asset_comment, name='asset-comment'),
    path('login/', auth_views.LoginView.as_view(template_name='asset1/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
