from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Location(models.Model):
    name = models.CharField(max_length=120)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    STATUS_AVAILABLE = "available"
    STATUS_ASSIGNED = "assigned"
    STATUS_MAINTENANCE = "maintenance"
    STATUS_LOST = "lost"
    STATUS_RETIRED = "retired"

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, "Available"),
        (STATUS_ASSIGNED, "Assigned"),
        (STATUS_MAINTENANCE, "Maintenance"),
        (STATUS_LOST, "Lost"),
        (STATUS_RETIRED, "Retired"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="assets")
    serial_number = models.CharField(max_length=200, blank=True, null=True, unique=True)
    description = models.TextField(blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="assigned_assets")
    acquired_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def assign(self, user, note=""):
        old = self.assigned_to
        self.assigned_to = user
        self.status = self.STATUS_ASSIGNED
        self.save()
        AssignmentHistory.objects.create(asset=self, assigned_from=old, assigned_to=user, note=note)

    def unassign(self, note=""):
        old = self.assigned_to
        self.assigned_to = None
        self.status = self.STATUS_AVAILABLE
        self.save()
        AssignmentHistory.objects.create(asset=self, assigned_from=old, assigned_to=None, note=note)

    def __str__(self):
        return f"{self.name}"

class AssignmentHistory(models.Model):

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="history")
    assigned_from = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                      on_delete=models.SET_NULL, related_name="+")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+")
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.asset.name} → {self.assigned_to}"
class AssetRequest(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="asset_requests")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    receive_at = models.DateTimeField(auto_now=True)

   
class IssueReport(models.Model):
    TYPE_DAMAGE = "damage"
    TYPE_LOST = "lost"
    TYPE_MAINTENANCE = "maintenance"
    TYPE_OTHER = "other"

    TYPE_CHOICES = [
        (TYPE_DAMAGE, "Damage"),
        (TYPE_LOST, "Lost"),
        (TYPE_MAINTENANCE, "Maintenance"),
        (TYPE_OTHER, "Other"),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="issues")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    issue_type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    description = models.TextField()
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def mark_resolved(self):
        self.resolved = True
        self.resolved_at = timezone.now()
        self.save()

class EmployeeList(models.Model):
    img = models.ImageField(upload_to='employee_images/', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return f"{self.id}"

