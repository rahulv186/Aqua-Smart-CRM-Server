import uuid
from django.db import models
from django.urls import reverse

# Create your models here.

class CustomerUserProfile(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="customer_user_profile")
    company = models.ForeignKey("companys.Company", on_delete=models.CASCADE, related_name="customer_user_profile")
    customer_code = models.CharField(max_length=50, unique=True, default="")

    name = models.CharField(max_length=150, blank=True, null=True)
    addressLine1 = models.TextField(max_length=255, blank=True, null=True)
    addressLine2 = models.TextField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    alternate_contact = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#   assets       Asset[]
#   serviceJobs  ServiceJob[]
    # jobs = models.ForeignKey("jobs.Job_card", on_delete=models.SET_NULL, blank=True, null=True)
#   complaints   Complaint[]
    amc_contract = models.ForeignKey("amc.amc_contract", on_delete=models.SET_NULL, blank=True, null=True)
    # invoices = models.ForeignKey("invoice.invoice", on_delete=models.SET_NULL, blank=True, null=True, related_name="customer_invoices")
#   payments     Payment[]
#   files        FileObject[]


    class Meta:
        db_table = "customer_user_profiles"
        ordering = ["name"]

    def __str__(self):
        return self.name


