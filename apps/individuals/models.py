from django.db import models

class IndividualCreditProfile(models.Model):
    full_name=models.CharField(max_length=255)
    yearly_income=models.FloatField()
    existing_debt=models.FloatField()
    collateral_value=models.FloatField()


    #ml output field
    risk_score=models.FloatField(null=True, blank=True)
    explanation=models.JSONField(null=True, blank=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name