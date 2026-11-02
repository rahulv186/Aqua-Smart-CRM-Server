import uuid

from django.db import models
from django.urls import reverse

# Create your models here.
import uuid
from django.db import models
from django_fsm import FSMField, transition
from companys.models import Company
from customers.models import CustomerUserProfile

class Customer_RO_Purifier(models.Model):
    class PurifierStatus(models.TextChoices):
        IN_WAREHOUSE = 'in_warehouse', 'In Warehouse'
        INSTALLED = 'installed', 'Installed'
        OUT_OF_SERVICE = 'out_of_service', 'Out of Service'
        DECOMMISSIONED = 'decommissioned', 'Decommissioned'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='purifiers')
    
    # Hardware / Model Details
    model_number = models.CharField(max_length=100, help_text="e.g., Kent Grand+, Aquaguard Aura", default="Unknown Model")
    serial_number = models.CharField(max_length=100, unique=True, help_text="Unique barcode/QR serial number")
    capacity = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 10L, 15L/hr")
    
    # Assignment (Null when sitting in the warehouse, populated upon installation)
    customer = models.ForeignKey(
        CustomerUserProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='purifiers'
    )
    
    # Lifecycle State Management (django-fsm)
    status = FSMField(
        default=PurifierStatus.IN_WAREHOUSE, 
        choices=PurifierStatus.choices, 
        protected=True
    )
    
    installation_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('company', 'serial_number')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.model_number} ({self.serial_number}) - {self.status}"

    # FSM Transitions
    @transition(field=status, source=PurifierStatus.IN_WAREHOUSE, target=PurifierStatus.INSTALLED)
    def install_unit(self, customer_profile, install_date):
        self.customer = customer_profile
        self.installation_date = install_date

