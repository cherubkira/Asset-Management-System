from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "asset1"

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assets/', views.asset_list, name='asset_list'),
    path('create/', views.asset_create, name='asset-create'),
    path('assets/history/', views.asset_history, name='asset_history'),
    path('assets/request/', views.asset_request, name='asset_request'),
    path('employees/', views.employee_list, name='employee_list'),
    path('assets/detail/', views.asset_detail, name='asset-detail'),
    path('assets/subcategory/', views.asset_subcategory, name='asset-subcategory'),
    path('assets/status/', views.asset_status, name='asset-status'),
    path('assets/comment/', views.asset_comment, name='asset-comment'),
    path('login/', auth_views.LoginView.as_view(template_name='asset1/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
