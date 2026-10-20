import uuid

from django.db import models
from django.urls import reverse

# Create your models here.


class inventory_item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="inventory_items")
    item_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    batch_code = models.CharField(max_length = 100, blank=True, null=True)
    item_image = models.ForeignKey("files.files", on_delete=models.SET_NULL, related_name="inventory_item", blank=True, null=True)
    item_type = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    bought_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    class Meta:
        verbose_name = ("inventory_item")
        verbose_name_plural = ("inventory_items")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("inventory_item_detail", kwargs={"pk": self.pk})
