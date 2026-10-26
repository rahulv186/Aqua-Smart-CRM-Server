from django.db import models
from django_fsm import FSMField, transition
import uuid
from django.urls import reverse


class ServiceTicket(models.Model):
    class TicketType(models.TextChoices):
        AD_HOC = 'AD_HOC', 'Customer Service Request'
        AMC = 'AMC', 'Annual Maintenance Contract Visit'

    class TicketState(models.TextChoices):
        OPEN = 'OPEN', 'Open / Unassigned'
        ASSIGNED = 'ASSIGNED', 'Technician Assigned'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_type = models.CharField(max_length=20, choices=TicketType.choices, default=TicketType.AD_HOC)
    
    # Relationships
    customer = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="service_tickets")
    purifier = models.ForeignKey("devices.ROPurifier", on_delete=models.CASCADE, related_name="tickets")
    
    # The assigned technician (Nullable initially until the manager assigns one)
    technician = models.ForeignKey(
        "technicians.TechnicianUserProfile", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="assigned_tickets"
    )
    
    issue_description = models.TextField(blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    
    # State Machine Field
    state = FSMField(default=TicketState.OPEN, choices=TicketState.choices, protected=True)

    # --- MANAGER / TECHNICIAN WORKFLOW TRANSITIONS ---

    @transition(field=state, source=TicketState.OPEN, target=TicketState.ASSIGNED)
    def assign_to_technician(self, technician, scheduled_date):
        """Manager assigns a technician and schedules the visit date/time."""
        self.technician = technician
        self.scheduled_date = scheduled_date

    @transition(field=state, source=TicketState.ASSIGNED, target=TicketState.IN_PROGRESS)
    def start_job(self):
        """Technician arrives on-site and starts work."""
        pass

    @transition(field=state, source=[TicketState.ASSIGNED, TicketState.IN_PROGRESS], target=TicketState.COMPLETED)
    def complete_job(self):
        """Technician marks the service or AMC job as finished."""
        # Optional: Reset/update purifier filter health metrics here if filters were replaced
        pass

    class Meta:
        db_table = "service_tickets"
        ordering = ["-created_at"]



















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

