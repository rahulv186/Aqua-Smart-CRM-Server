from rest_framework import serializers
from .models import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "name",
            "sku",
            "category",
            "stock_quantity",
            "min_stock_level",
            "unit_price"
        ]
        read_only_fields = ["id"]
