import uuid
from django.db import models
from companys.models import Company

class InventoryItem(models.Model):
    class Category(models.TextChoices):
        FILTERS = "FILTERS", "Filters"
        MEMBRANES = "MEMBRANES", "Membranes"
        PUMPS_ELECTRICAL = "PUMPS_ELECTRICAL", "Pumps/Electrical"
        FITTINGS = "FITTINGS", "Fittings"
        SPARE_PARTS = "SPARE_PARTS", "Other Spare Parts"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="inventory_items")
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100)
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.SPARE_PARTS
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "sku")
        ordering = ["name"]
        db_table = "inventory_items"

    def __str__(self):
        return f"{self.name} ({self.sku}) - {self.company.company_name}"
