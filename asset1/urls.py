from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "asset1"

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('contact/', views.contact_view, name='contact_view'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assets/', views.asset_list, name='asset_list'),
    path('asset/create/', views.asset_create, name='asset-create'),
    path('asset/employees/', views.employee_list, name='employee_list'),
    path('asset/employees/add/', views.employee_create, name='employee_create'),
    path('assets/history/', views.asset_history, name='asset_history'),

    path('assets/category/', views.category_list, name='asset_category'),
    path('assets/category/add/', views.category_create, name='category_create'),
    path("asset/Subcategory/", views.subcategory_list, name="subcategory_list"),
    path("asset/Subcategory/add/", views.subcategory_create, name="subcategory_create"),
    path('asset/status/', views.asset_status, name='asset_status'),
    path('asset/delete/<int:pk>/', views.asset_delete, name='asset_delete'),
    path('asset/requests/', views.asset_request_list, name='asset_request_list'),
    path('asset/issues/', views.asset_issue_list, name='asset_issue_list'),
    path("asset/<int:pk>/update/", views.asset_update, name="asset-update"),
   
    path('assets/detail/<int:id>/', views.asset_detail, name='asset-detail'),

    path('login/', auth_views.LoginView.as_view(template_name='asset1/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
