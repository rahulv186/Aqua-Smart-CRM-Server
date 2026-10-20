import uuid

from django.db import models
from django.urls import reverse

# Create your models here.
class ManagerUserProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    organization_id = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="managers")
    addressLine1 = models.TextField(blank=True, max_length=255)
    addressLine2 = models.TextField(blank=True, max_length=255)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = "manager_user_profiles"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ManagerUserProfile_detail", kwargs={"pk": self.pk})
