import uuid
from django.db import models
from django.urls import reverse

# Create your models here.#

class CustomerUserProfile(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    userid = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="customer_user_profile")
    organization_id = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="customer_user_profile")
    customer_code = models.CharField(max_length=50, unique=True)

    name = models.CharField(max_length=150)
    addressLine1 = models.TextField(blank=True, max_length=255)
    addressLine2 = models.TextField(blank=True, max_length=255)
    age = models.PositiveIntegerField(null=True, blank=True)
    alternate_contact = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#   assets       Asset[]
#   serviceJobs  ServiceJob[]
#   complaints   Complaint[]
#   amcContracts AmcContract[]
#   invoices     Invoice[]
#   payments     Payment[]
#   files        FileObject[]


    class Meta:
        verbose_name = ("CustomerUserProfile")
        verbose_name_plural = ("CustomerUserProfiles")

    def __str__(self):
        return self.name

