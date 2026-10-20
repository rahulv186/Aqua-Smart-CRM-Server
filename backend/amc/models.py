import uuid

from django.db import models
from django.urls import reverse

# Create your models here.


class amc_contract(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="amc_contracts")
    contract_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    customer_id = models.ForeignKey("customers.CustomerUserProfile", on_delete=models.CASCADE, related_name="amc_contracts")
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    last_service_date = models.DateField(blank=True, null=True)
    next_service_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    visit_frequency = models.IntegerField(blank=True, null=True)
    visit_count = models.IntegerField(blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    

    class Meta:

        db_table = "amc_contracts"
        ordering = ["id"]
        unique_together = ("organization_id", "contract_number")

    def __str__(self):
        return self.contract_number

    def get_absolute_url(self):
        return reverse("amc_contract_detail", kwargs={"pk": self.pk})


class amc_visit(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="amc_visits", blank=True, null=True)
    contract_id = models.ForeignKey("amc.amc_contract", on_delete=models.CASCADE, related_name="amc_visits", blank=True, null=True)
    visit_date = models.DateField(blank=True, null=True)
    # job_id
    technician = models.ForeignKey("technicians.TechnicianUserProfile", on_delete=models.CASCADE, related_name="amc_visits", blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    # invoice





    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    

    class Meta:
        db_table = "amc_visits"
        ordering = ["id"]


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("amc_visit_detail", kwargs={"pk": self.pk})
