from django.db import models

class CreditRequest(models.Model):
    APPLICANT_INDIVIDUAL = "individual"
    APPLICANT_COMPANY = "company"
    APPLICANT_CHOICES = [
        (APPLICANT_INDIVIDUAL, "Individual"),
        (APPLICANT_COMPANY, "Company"),
    ]

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    applicant_type = models.CharField(max_length=20, choices=APPLICANT_CHOICES)
    # Use "app_label.ModelName" strings for lazy references
    individual = models.ForeignKey(
        "individuals.IndividualCreditProfile",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="credit_requests",
    )
    company = models.ForeignKey(
        "companies.CompanyCreditProfile",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="credit_requests",
    )

    requested_amount = models.BigIntegerField()
    term_months = models.IntegerField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    # Results from scoring
    score = models.IntegerField(null=True, blank=True)
    model_version = models.CharField(max_length=128, null=True, blank=True)
    explanation = models.JSONField(null=True, blank=True)  # store last prediction explanation

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Credit Request"
        verbose_name_plural = "Credit Requests"

    def __str__(self):
        return f"CreditRequest({self.id}) {self.applicant_type} amount={self.requested_amount}"