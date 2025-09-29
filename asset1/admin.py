from django.contrib import admin
from .models import Category, Location, Asset, AssignmentHistory, AssetRequest, IssueReport

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "status", "assigned_to", "location", "serial_number"]
    search_fields = ["name", "serial_number"]
    list_filter = ["status", "category", "location"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (None, {"fields": ("name","category","serial_number","description")}),
        ("Logistics", {"fields": ("location","acquired_date","purchase_price")}),
        ("Assignment", {"fields": ("assigned_to","status")}),
        ("Meta", {"fields": ("is_active","created_at","updated_at")}),
    )

@admin.register(AssignmentHistory)
class AssignmentHistoryAdmin(admin.ModelAdmin):
    list_display = ["asset", "assigned_from", "assigned_to", "created_at"]
    readonly_fields = ["created_at"]

@admin.register(AssetRequest)
class AssetRequestAdmin(admin.ModelAdmin):
    list_display = ["requester","category","asset","status","created_at"]
    list_filter = ["status","category"]

@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):
    list_display = ["asset","reporter","issue_type","resolved","created_at"]
    list_filter = ["issue_type","resolved"]


# Register your models here.
