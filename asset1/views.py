from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Asset, AssignmentHistory, AssetRequest, IssueReport
from .forms import AssetForm
from django.core.paginator import Paginator



def landing_page(request):
    if request.user.is_authenticated:   
        return redirect('asset1:dashboard')
    return render(request, 'asset1/landing.html')


@login_required
def dashboard(request):
    total_assets = Asset.objects.filter(is_active=True).count()
    available = Asset.objects.filter(status=Asset.STATUS_AVAILABLE, is_active=True).count()
    assigned = Asset.objects.filter(status=Asset.STATUS_ASSIGNED, is_active=True).count()
    pending_requests = AssetRequest.objects.filter(status=AssetRequest.STATUS_PENDING).count()

    recent_history = list(
        AssignmentHistory.objects.select_related("asset", "assigned_to", "assigned_from")
        .order_by('-created_at')[:10]
    )
     
    
    context = {
        "total_assets": total_assets,
        "available": available,
        "assigned": assigned,
        "pending_requests": pending_requests,
        "recent_assignments": recent_history,

    }
    return render(request, 'asset1/dashboard.html', context)


@login_required
def asset_list(request):
    
    assets = Asset.objects.select_related("assigned_to", "category").all()
    find_asset = request.GET.get("find_asset")
    
    if find_asset:
        assets = assets.filter(name__icontains= find_asset)

    
    paginator = Paginator(assets, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    
    context = {
        "object_list": page_obj,   
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
        "search_query": find_asset or "",
    }
    return render(request, "asset1/asset_list.html", context)

@login_required
def asset_history(request):
    history = AssignmentHistory.objects.select_related("asset","assigned_to").all()
    return render(request, 'asset1/asset_history.html', {"history": history})

@login_required
def asset_detail(request):
    
    return render(request, 'asset1/asset-detail.html')

@login_required
def asset_subcategory(request):
    
    return render(request, 'asset1/asset_subcategory.html')

@login_required
def asset_status(request):
    
    return render(request, 'asset1/asset_status.html')

@login_required
def asset_comment(request):
    
    return render(request, 'asset1/asset_comment.html')

@login_required
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset1:asset_list')
    else:
        form = AssetForm()
    return render(request, 'asset1/asset_form.html', {'form': form})

@login_required
def asset_request(request):
    object_list = AssetRequest.objects.select_related("requester","category", "asset").all()
    return render(request, 'asset1/request_list.html',{"object_list": object_list})

@login_required
def employee_list(request):
    return render(request, 'asset1/employee_list.html')