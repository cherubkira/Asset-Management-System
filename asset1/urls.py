from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = "asset1"

urlpatterns = [
    path("", views.LandingView.as_view(), name="landing"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("asset1/", views.AssetListView.as_view(), name="asset-list"),
    path("asset1/create/", views.AssetCreateView.as_view(), name="asset-create"),
    path("asset1/<int:pk>/", views.AssetDetailView.as_view(), name="asset-detail"),
    path("asset1/<int:pk>/edit/", views.AssetUpdateView.as_view(), name="asset-edit"),
    path("asset1/<int:pk>/delete/", views.AssetDeleteView.as_view(), name="asset-delete"),
    path("asset1/<int:pk>/assign/", views.AssignAssetView.as_view(), name="asset-assign"),
    path("requests/", views.RequestListView.as_view(), name="request-list"),
    path("requests/create/", views.RequestCreateView.as_view(), name="request-create"),
    path("issues/", views.IssueListView.as_view(), name="issue-list"),
    path("issues/create/", views.IssueCreateView.as_view(), name="issue-create"),
    path('accounts/login/', LoginView.as_view(template_name='asset1/login.html'), name='login'),
     path("accounts/logout/",LogoutView.as_view(next_page="asset1:landing"),name="logout",
    ),
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/history/', views.asset_history, name='asset_history'),
    path('assets/categories/', views.asset_category, name='asset_category'),
    path('assets/subcategories/', views.asset_subcategory, name='asset_subcategory'),
    path('assets/status/', views.asset_status, name='asset_status'),
    path('assets/comments/', views.asset_comment, name='asset_comment'),
    path("assets/create/", views.asset_create, name="asset_create"),
]
    

 