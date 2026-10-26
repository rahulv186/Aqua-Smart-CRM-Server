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
    purifier = models.ForeignKey("assets.Customer_RO_Purifier", on_delete=models.CASCADE, related_name="tickets")
    
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

    created_at = models.DateTimeField(auto_now_add=True)

    # --- MANAGER / TECHNICIAN WORKFLOW TRANSITIONS ---

    @transition(field=state, source=TicketState.OPEN, target=TicketState.ASSIGNED)
    def assign_to_technician(self, technician, scheduled_date):
        """Manager assigns a technician and schedules the visit date/time."""
        self.technician = technician
        self.scheduled_date = scheduled_date

    @transition(field=state, source=TicketState.ASSIGNED, target=TicketState.IN_PROGRESS)
    def start_job(self):
        """Technician arrives on-site and starts work."""
        # self.state = self.TicketState.IN_PROGRESS

    @transition(field=state, source=[TicketState.ASSIGNED, TicketState.IN_PROGRESS], target=TicketState.COMPLETED)
    def complete_job(self):
        """Technician marks the service or AMC job as finished."""
        # Optional: Reset/update purifier filter health metrics here if filters were replaced
        pass
    class Meta:
        db_table = "service_tickets"
        ordering = ["-created_at"]


