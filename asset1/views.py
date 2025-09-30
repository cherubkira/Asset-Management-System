from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Asset, AssignmentHistory, AssetRequest, IssueReport
from .forms import AssetForm

# Landing page
def landing_page(request):
    if request.user.is_authenticated:   # redirect logged-in users to dashboard
        return redirect('asset1:dashboard')
    return render(request, 'asset1/landing.html')

# Dashboard
@login_required
def dashboard(request):
    total_assets = Asset.objects.filter(is_active=True).count()
    available = Asset.objects.filter(status=Asset.STATUS_AVAILABLE, is_active=True).count()
    assigned = Asset.objects.filter(status=Asset.STATUS_ASSIGNED, is_active=True).count()
    pending_requests = AssetRequest.objects.filter(status=AssetRequest.STATUS_PENDING).count()
    recent_assignments = AssignmentHistory.objects.select_related("asset","assigned_to").order_by('-created_at')[:10]

    context = {
        "total_assets": total_assets,
        "available": available,
        "assigned": assigned,
        "pending_requests": pending_requests,
        "recent_assignments": recent_assignments,
    }
    return render(request, 'asset1/dashboard.html', context)

# Simple asset pages (list, history, category, etc.)
@login_required
def asset_list(request):
    assets = Asset.objects.filter(is_active=True).select_related("category","location","assigned_to")
    return render(request, 'asset1/asset_list.html', {"assets": assets})

@login_required
def asset_history(request):
    history = AssignmentHistory.objects.select_related("asset","assigned_to").all()
    return render(request, 'asset1/asset_history.html', {"history": history})

@login_required
def asset_category(request):
    # Add logic if needed
    return render(request, 'asset1/asset_category.html')

@login_required
def asset_subcategory(request):
    # Add logic if needed
    return render(request, 'asset1/asset_subcategory.html')

@login_required
def asset_status(request):
    # Add logic if needed
    return render(request, 'asset1/asset_status.html')

@login_required
def asset_comment(request):
    # Add logic if needed
    return render(request, 'asset1/asset_comment.html')

@login_required
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset1:asset-list')
    else:
        form = AssetForm()
    return render(request, 'asset1/asset_form.html', {'form': form})