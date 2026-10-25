import uuid

from django.db import models
from django.urls import reverse

# Create your models here.

class invoice_file(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companys.Company', on_delete=models.CASCADE, related_name='company_invoice_files')
    invoice_id = models.ForeignKey('invoice.invoice', on_delete=models.CASCADE, related_name='invoice_files')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='invoices/')
    uploaded_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='uploaded_invoice_files')
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    size_bytes = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = ("file")
        verbose_name_plural = ("files")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("file_detail", kwargs={"pk": self.pk})


class files(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.ForeignKey('companys.Company', on_delete=models.CASCADE, related_name='company_files')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='uploaded_files')
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    size_bytes = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("file")
        verbose_name_plural = ("files")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("file_detail", kwargs={"pk": self.pk})
