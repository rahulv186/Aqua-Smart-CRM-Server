import uuid

from django.db import models
from django.urls import reverse

# Create your models here.


class inventory_item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey("companys.Company", on_delete=models.CASCADE, related_name="inventory_items")
    item_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    batch_code = models.CharField(max_length = 100, blank=True, null=True)
    item_image = models.ForeignKey("files.files", on_delete=models.SET_NULL, related_name="inventory_item", blank=True, null=True)
    item_type = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    bought_at = models.DateTimeField()


    is_sold = models.BooleanField(default=False)
    sold_to = models.ForeignKey("customers.CustomerUserProfile", on_delete=models.SET_NULL, blank=True, null=True,  related_name="sold_to_customer")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    class Meta:
        verbose_name = ("inventory_item")
        verbose_name_plural = ("inventory_items")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("inventory_item_detail", kwargs={"pk": self.pk})



class Customer_RO_Purifier(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey("companys.Company", on_delete=models.CASCADE, related_name="ro_purifiers")
    item_code = models.CharField(max_length=10, unique=True)
    customer = models.ForeignKey("customers.CustomerUserProfile", on_delete=models.SET_NULL, related_name="ro_unit", null=True, blank=True)
    serial_number = models.CharField(max_length=50, unique=True)
    model_name = models.CharField(max_length=255)
    capacity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Capacity in litres")
    purchase_date = models.DateField(blank=True)
    installation_date = models.DateField(blank=True)
    warranty = models.PositiveIntegerField(blank=True)
    warranty_ending_date = models.DateField(blank=True)
    is_under_warranty = models.BooleanField(default=True)

    last_service_date = models.DateField(blank=True)

    has_amc_contract = models.BooleanField(default=False)
    amc_contract = models.ForeignKey("amc.amc_contract", on_delete=models.SET_NULL, blank=True, null=True, related_name="customer_ro_unit")
    amc_is_active = models.BooleanField(default=False)


    # IOT device endpoint
    # telemetry = models.ForeignKey


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Customer_RO_Purifier")
        verbose_name_plural = ("Customer_RO_Purifiers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Customer_RO_Purifier_detail", kwargs={"pk": self.pk})
