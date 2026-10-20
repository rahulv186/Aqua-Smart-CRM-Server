import uuid

from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class TechnicianUserProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name="technician_user_profile")
    organization_id = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="technicians")
    employee_code = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    emergency_contact = models.CharField(max_length=20, blank=True)
    addressLine1 = models.TextField(blank=True, max_length=255)
    addressLine2 = models.TextField(blank=True, max_length=255)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    skills = ArrayField(models.CharField(max_length=100), blank=True, default=list)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = "technician_user_profiles"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("TechUserProfile_detail", kwargs={"pk": self.pk})
