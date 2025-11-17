from django.db import models

class IndividualCreditProfile(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    yearly_income = models.BigIntegerField(null=True, blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    existing_debt = models.BigIntegerField(null=True, blank=True)
    collateral_value = models.BigIntegerField(null=True, blank=True)
    property_net_worth = models.BigIntegerField(null=True, blank=True)

    guarantor_info = models.JSONField(null=True, blank=True)  # {name, inn, phone}
    credit_history_score = models.IntegerField(null=True, blank=True)
    criminal_history = models.BooleanField(default=False)

    soliq_record = models.JSONField(null=True, blank=True)   # mocked gov data
    kadastr_record = models.JSONField(null=True, blank=True) # mocked land registry

    requested_amount = models.BigIntegerField(null=True, blank=True)
    term_months = models.IntegerField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    score = models.IntegerField(null=True, blank=True)  # store last computed score
    model_version = models.CharField(max_length=128, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Individual Credit Profile"
        verbose_name_plural = "Individual Credit Profiles"

    def __str__(self):
        return f"{self.full_name} ({self.id})"