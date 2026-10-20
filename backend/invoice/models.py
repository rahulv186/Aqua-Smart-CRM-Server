import uuid

from django.db import models
from django.urls import reverse

# Create your models here.

class invoice(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey("companys.Company", on_delete=models.CASCADE, related_name="invoices")
    invoice_number = models.CharField(max_length=50, unique=True)
    customer_id = models.ForeignKey("customers.CustomerUserProfile", on_delete=models.CASCADE, related_name="invoices")
    created_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="created_invoices")
    issue_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    

    class Meta:
        verbose_name = ("Invoice")
        verbose_name_plural = ("Invoices")
        db_table = "invoices"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Invoice_detail", kwargs={"pk": self.pk})


class invoice_item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_id = models.ForeignKey("invoice", on_delete=models.CASCADE, related_name="invoice_items")
    # item_id = models.ForeignKey("items.Item", on_delete=models.CASCADE, related_name="invoice_items")
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = ("invoice_item")
        verbose_name_plural = ("invoice_items")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("invoice_item_detail", kwargs={"pk": self.pk})
