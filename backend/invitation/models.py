from django.db import models
import uuid
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey("companys.Company", on_delete=models.CASCADE, related_name="invitations")
    email = models.CharField(max_length=150)
    token = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
            if not self.expires_at:
                #  1 day expiry
                self.expires_at = timezone.now() + timedelta(days=1)
            super().save(*args, **kwargs)

    def is_valid(self):
            return not self.is_accepted and timezone.now() <= self.expires_at

    def __str__(self):
            return f"Invite for {self.email} to {self.company.name}"    

    