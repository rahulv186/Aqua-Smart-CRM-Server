import uuid

from django.db import models
from django.urls import reverse

# Create your models here.


class job_card(models.Model):




    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_card_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    customer_id = models.ForeignKey("customers.CustomerUserProfile", on_delete=models.CASCADE, related_name="job_cards")
    created_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="created_job_cards")
    technician_id = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, related_name="assigned_job_cards", blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)

    completed_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False, blank=True)
    invoice_id = models.ForeignKey("invoice.invoice", on_delete=models.SET_NULL, related_name="job_cards", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = ("job_card")
        verbose_name_plural = ("job_cards")
        db_table = "job_cards"

    def __str__(self):
        return self.job_card_id

    def get_absolute_url(self):
        return reverse("job_card_detail", kwargs={"pk": self.pk})


class job_assignment(models.Model):

    JOB_TYPE_CHOICES = [
        ("installation", "Installation"),
        ("maintenance", "Maintenance"),
        ("repair", "Repair"),
        ("inspection", "Inspection"),
        ("replacement", "Replacement"),
        ("amc", "AMC"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    technician_id = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="job_assignments")
    scheduled_date = models.DateTimeField(blank=True, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    job_type = models.CharField(max_length=100, blank=True, choices=JOB_TYPE_CHOICES) 


    class Meta:
        verbose_name = ("job_assignment")
        verbose_name_plural = ("job_assignments")
        db_table = "job_assignments"

    def __str__(self):
        return f"Assignment for Job Card {self.job_card_id} to Technician {self.technician_id}"


class Jobstatusevent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_card_id = models.ForeignKey("job_card", on_delete=models.CASCADE, related_name="job_status_events", blank=True, null=True)
    fromstatus = models.CharField(max_length=100, blank=True)
    tostatus = models.CharField(max_length=100, blank=True)
    changed_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, related_name="job_status_changes", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        db_table = 'JobStatusEvent'

