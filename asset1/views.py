from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db import models
from .models import Asset, AssignmentHistory, AssetRequest, IssueReport, Category
from .forms import AssetForm, AssetRequestForm, IssueReportForm
from .filters import AssetFilter
from django.core.paginator import Paginator

# Landing page
class LandingView(generic.TemplateView):
    template_name = "asset1/landing.html"

# Dashboard
class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "asset1/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["total_assets"] = Asset.objects.filter(is_active=True).count()
        ctx["available"] = Asset.objects.filter(status=Asset.STATUS_AVAILABLE, is_active=True).count()
        ctx["assigned"] = Asset.objects.filter(status=Asset.STATUS_ASSIGNED, is_active=True).count()
        ctx["pending_requests"] = AssetRequest.objects.filter(status=AssetRequest.STATUS_PENDING).count()
        ctx["recent_assignments"] = AssignmentHistory.objects.select_related("asset","assigned_to").all()[:10]
        return ctx

# Asset list with filtering
class AssetListView(LoginRequiredMixin, generic.ListView):
    model = Asset
    template_name = "asset1/asset_list.html"
    paginate_by = 20

    def get_queryset(self):
        qs = Asset.objects.filter(is_active=True).select_related("category","location","assigned_to")
        self.filter_set = AssetFilter(self.request.GET, queryset=qs)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter"] = self.filter_set
        return ctx

class AssetDetailView(LoginRequiredMixin, generic.DetailView):
    model = Asset
    template_name = "asset1/asset_detail.html"

class AssetCreateView(PermissionRequiredMixin, generic.CreateView):
    model = Asset
    form_class = AssetForm
    template_name = "asset1/asset_form.html"
    success_url = reverse_lazy("asset1:asset-list")
    permission_required = "asset1.add_asset"

class AssetUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = "asset1/asset_form.html"
    success_url = reverse_lazy("asset1:asset-list")
    permission_required = "asset1.change_asset"

class AssetDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Asset
    template_name = "asset1/asset_confirm_delete.html"
    success_url = reverse_lazy("asset1:asset-list")
    permission_required = "asset1.delete_asset"

# assign/reassign simple view
class AssignAssetView(PermissionRequiredMixin, generic.FormView):
    permission_required = "asset1.change_asset"
    template_name = "asset1/assign_form.html"
    form_class = AssetForm  # reuse for simplicity
    success_url = reverse_lazy("asset1:asset-list")

    def form_valid(self, form):
        asset_pk = self.kwargs.get("pk")
        asset = get_object_or_404(Asset, pk=asset_pk)
        user = form.cleaned_data.get("assigned_to")
        note = "Assigned via AssignAssetView"
        asset.assign(user, note=note)
        return super().form_valid(form)

# Requests
class RequestListView(LoginRequiredMixin, generic.ListView):
    model = AssetRequest
    template_name = "asset1/request_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return AssetRequest.objects.all().select_related("requester","category","asset")
        return AssetRequest.objects.filter(requester=user)

class RequestCreateView(LoginRequiredMixin, generic.CreateView):
    model = AssetRequest
    form_class = AssetRequestForm
    template_name = "asset1/request_form.html"
    success_url = reverse_lazy("asset1:request-list")

    def form_valid(self, form):
        form.instance.requester = self.request.user
        return super().form_valid(form)

# Issues
class IssueListView(LoginRequiredMixin, generic.ListView):
    model = IssueReport
    template_name = "asset1/issue_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return IssueReport.objects.all().select_related("asset","reporter")
        return IssueReport.objects.filter(reporter=user)

class IssueCreateView(LoginRequiredMixin, generic.CreateView):
    model = IssueReport
    form_class = IssueReportForm
    template_name = "asset1/issue_form.html"
    success_url = reverse_lazy("asset1:issue-list")

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)




