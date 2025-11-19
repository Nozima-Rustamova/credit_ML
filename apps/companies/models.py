from django.db import models

class CompanyCreditProfile(models.Model):
    # add these constants and field inside CompanyCreditProfile model
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
    (STATUS_PENDING, "Pending"),
    (STATUS_APPROVED, "Approved"),
    (STATUS_REJECTED, "Rejected"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    company_name=models.CharField(max_length=255)
    tax_id=models.CharField(max_length=100, null=True, blank=True)
    incorporated_date=models.DateField(null=True, blank=True)
    industry=models.CharField(max_length=100, null=True, blank=True)
    years_in_business = models.IntegerField(null=True, blank=True)
    revenue = models.BigIntegerField(null=True, blank=True)
    net_income = models.BigIntegerField(null=True, blank=True)
    assets = models.BigIntegerField(null=True, blank=True)
    liabilities = models.BigIntegerField(null=True, blank=True)

    financial_statements = models.JSONField(null=True, blank=True)
    financial_ratios = models.JSONField(null=True, blank=True)

    contact_person = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    score = models.IntegerField(null=True, blank=True)
    model_version = models.CharField(max_length=128, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} ({self.id})"