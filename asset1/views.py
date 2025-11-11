from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Asset, AssignmentHistory, AssetRequest, IssueReport
from .forms import AssetForm
from django.core.paginator import Paginator
from .models import EmployeeList,Category,SubCategory,IssueReport
from .forms import EmployeeForm, CategoryForm, SubCategoryForm, AssetRequestForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model




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
    
    recent_employees = EmployeeList.objects.order_by('id')[:10]

    assigned_percentage = (assigned / total_assets * 100) if total_assets else 0

    context = {
        "total_assets": total_assets,
        "available": available,
        "assigned": assigned,
        "pending_requests": pending_requests,
        "recent_assignments": recent_history,
        "employees": recent_employees,
        "assigned_percentage": round(assigned_percentage, 2),  
    }
    return render(request, 'asset1/dashboard.html', context)


@login_required
def asset_list(request):
    
    
    find_asset = request.GET.get("find_asset","") 

    assets = Asset.objects.select_related("assigned_to", "category").filter(
        Q(name__icontains=find_asset) 
        | Q(category__name__icontains=find_asset)
        | Q(status__icontains=find_asset)
        | Q(id__icontains=find_asset
    ))
    
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
    
    return render(request, 'asset1/asset_detail.html')

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
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('asset1:employee_create')
    else:
        form = EmployeeForm()
    return render(request, 'asset1/employee_list_form.html', {'form': form})

def employee_list(request):
    employees = EmployeeList.objects.all()
    return render(request, 'asset1/employee_list.html', {'employees': employees})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'asset1/asset_category.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset1:category_list')
    else:
        form = CategoryForm()
    return render(request, 'asset1/asset_category_create.html', {'form': form})


def subcategory_create(request):
    if request.method == "POST":
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("asset1:subcategory_list")
    else:
        form = SubCategoryForm()
    return render(request, "asset1/asset_subc_list.html", {"form": form})

def subcategory_list(request):
    subcategories = SubCategory.objects.all()
    return render(request, "asset1/asset_subca.html", {"subcategories": subcategories})

@login_required
def asset_status(request):
    assets = Asset.objects.all().order_by('id')
    return render(request, 'asset1/asset_status.html', {'assets': assets})

@login_required
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "POST":
        asset.delete()
        messages.success(request, "Asset deleted successfully.")
        return redirect("asset1:asset_status")  

    
    return redirect("asset1:asset_status")


def asset_request_list(request):
    
    requests = AssetRequest.objects.select_related('asset', 'requester', 'category').all().order_by('-requested_at')
    return render(request, 'asset1/request_list.html', {'requests': requests})


def asset_issue_list(request):
    issues = IssueReport.objects.select_related("asset", "reporter").all().order_by('-created_at')
    return render(request, "asset1/issue_list.html", {"issues": issues,})

def asset_update(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == "POST":
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect("asset1:asset_list")
    else:
        form = AssetForm(instance=asset)
    return render(request, "asset1/asset_form.html", {"form": form})
