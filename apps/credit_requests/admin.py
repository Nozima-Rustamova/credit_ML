from django.contrib import admin
from .models import CreditRequest

@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant_type', 'individual', 'company', 'requested_amount', 'status', 'score', 'created_at')
    list_filter = ('applicant_type', 'status', 'created_at')
    search_fields = ('individual__full_name', 'company__company_name',)