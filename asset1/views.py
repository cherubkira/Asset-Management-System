from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Asset, AssignmentHistory, AssetRequest, IssueReport
from .forms import AssetForm,ContactForm
from django.core.paginator import Paginator
from .models import EmployeeList,Category,SubCategory,IssueReport
from .forms import EmployeeForm, CategoryForm, SubCategoryForm, AssetRequestForm
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings


def landing_page(request):
   
    if request.user.is_authenticated:   
        return redirect('asset1:dashboard')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Website Contact Form Inquiry'
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message_body = "\n".join(body.values())

            try:
                send_mail(subject, message_body, settings.EMAIL_HOST_USER, ['your_recipient_email@example.com'])
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.error(request, f'There was an error sending your message: {e}')
            
            
            return redirect('asset1:landing') 
        else:
           
            contact_form = form
    else:

        contact_form = ContactForm()
    
    context = {'form': contact_form}
    return render(request, 'asset1/landing.html', context)

@login_required
def dashboard(request):
    total_assets = Asset.objects.filter(is_active=True).count()
    available = Asset.objects.filter(status=Asset.STATUS_AVAILABLE, is_active=True).count()
    assigned = Asset.objects.filter(status=Asset.STATUS_ASSIGNED, is_active=True).count()
    pending_requests = AssetRequest.objects.filter(status=AssetRequest.STATUS_PENDING).count()
    maintenance = Asset.objects.filter(status=Asset.STATUS_MAINTENANCE, is_active=True).count()

    recent_history = list(
        AssignmentHistory.objects.select_related("asset", "assigned_to", "assigned_from")
        .order_by('-created_at')[:10]
    )
    
    recent_employees = EmployeeList.objects.order_by('id')[:10]
    assigned_percentage = (assigned / total_assets * 100) if total_assets > 0 else 0

    context = {
        "total_assets": total_assets,
        "available": available,
        "assigned": assigned,
        "pending_requests": pending_requests,
        "maintenance": maintenance,
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

@login_required
def employee_list(request):
    query = request.GET.get('find_asset', '')  
    if query:
        employees = EmployeeList.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(department__icontains=query) |
            Q(id__icontains=query)
        )
    else:
        employees = EmployeeList.objects.all()

    return render(request, 'asset1/employee_list.html', {'employees': employees})

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'asset1/asset_category.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset1:category_list')
    else:
        form = CategoryForm()
    return render(request, 'asset1/asset_category_create.html', {'form': form})


@login_required
def subcategory_create(request):
    if request.method == "POST":
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("asset1:subcategory_list")
    else:
        form = SubCategoryForm()
    return render(request, "asset1/asset_subc_list.html", {"form": form})

@login_required
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


@login_required
def asset_request_list(request):
    requests = (
        AssetRequest.objects
        .select_related("requester", "category", "asset")
        .all()
        .order_by("-requested_at")
    )
    return render(request, "asset1/request_list.html", {"requests": requests})

@login_required
def create_asset_request(request):
    if request.method == "POST":
        form = AssetRequestForm(request.POST)
        if form.is_valid():
            asset_request = form.save(commit=False)
            asset_request.requester = request.user  
            asset_request.save()
            return redirect("asset1:request_list")
    else:
        form = AssetRequestForm()
    return render(request, "asset1/request_form.html", {"form": form})


@login_required
def asset_issue_list(request):
    issues = IssueReport.objects.select_related("asset", "reporter").all().order_by('-created_at')
    return render(request, "asset1/issue_list.html", {"issues": issues,})


@login_required
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


def contact_view(request):
     return redirect('asset1:landing_page') 
        