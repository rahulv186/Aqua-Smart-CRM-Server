import uuid

from django.db import models
from django.utils import timezone


class Organization(models.Model):

    PLANS = {("basic", "Basic"), ("standard", "Standard"), ("premium", "Premium")}

    PAYMENT_STATUS = {
        "pending": "Pending",
        "completed": "Completed",
        "failed": "Failed",
        "overdue": "Overdue",
    }

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,)

    organization_name = models.CharField(max_length=150)

    slug = models.SlugField(max_length=150,unique=True)

    phone = models.CharField(max_length=20,blank=True,null=True)

    email = models.EmailField(blank=True,null=True)

    gstin = models.CharField(max_length=20,blank=True,null=True)

    address = models.TextField(blank=True,null=True)

    city = models.CharField(max_length=100,blank=True,null=True)

    state = models.CharField(max_length=100,blank=True,null=True)

    postal_code = models.CharField(max_length=20,blank=True,null=True)

    timezone = models.CharField(max_length=50,default="Asia/Kolkata")

    currency = models.CharField(max_length=3,default="INR")

    plan = models.CharField(max_length=20,choices=PLANS,default="basic")

    plan_start_date = models.DateField(blank=True,null=True)

    plan_end_date = models.DateField(blank=True,null=True)

    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default="pending")

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True)


#   owner          OrganizationOwner?
#   managers       Manager[]
#   technicians    Technician[]
#   customers      Customer[]
#   assets         Asset[]
#   serviceJobs    ServiceJob[]
#   complaints     Complaint[]
#   amcContracts   AmcContract[]
#   reminders      Reminder[]
#   invoices       Invoice[]
#   payments       Payment[]
#   inventoryItems InventoryItem[]
#   stockMovements StockMovement[]
#   files          FileObject[]
#   auditLogs      AuditLog[]


    class Meta:
        db_table = "organizations"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

class OrganizationOwnerProfile(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user_id = models.UUIDField(unique=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name="owner")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = "organization_owners"
        ordering = ["created_at"]

    def __str__(self):
        return self.name

