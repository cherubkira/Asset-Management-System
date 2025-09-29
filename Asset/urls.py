from django.contrib import admin
from django.urls import path, include
from asset1 import views  # import app views

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    path('', include('asset1.urls', namespace='asset1')),

    # Landing & dashboard
    path("", views.LandingView.as_view(), name="landing"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),

    # Assets
    path("assets/", views.AssetListView.as_view(), name="asset-list"),
    path("assets/create/", views.AssetCreateView.as_view(), name="asset-create"),
    path("assets/<int:pk>/", views.AssetDetailView.as_view(), name="asset-detail"),
    path("assets/<int:pk>/edit/", views.AssetUpdateView.as_view(), name="asset-edit"),
    path("assets/<int:pk>/delete/", views.AssetDeleteView.as_view(), name="asset-delete"),
    path("assets/<int:pk>/assign/", views.AssignAssetView.as_view(), name="asset-assign"),

    # Requests
    path("requests/", views.RequestListView.as_view(), name="request-list"),
    path("requests/create/", views.RequestCreateView.as_view(), name="request-create"),

    # Issues
    path("issues/", views.IssueListView.as_view(), name="issue-list"),
    path("issues/create/", views.IssueCreateView.as_view(), name="issue-create"),

    # Auth (login/logout/password reset)
    path("accounts/", include("django.contrib.auth.urls")),
]
