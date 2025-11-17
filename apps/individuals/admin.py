from django.contrib import admin
from .models import IndividualCreditProfile

@admin.register(IndividualCreditProfile)
class IndividualCreditProfileAdmin(admin.ModelAdmin):
    list_display=('id', 'full_name', 'created_at', 'status', 'score', 'model_version')
    list_filter=('status', 'created_at', 'criminal_history')
    search_fields=('full_name', 'email', 'phone')