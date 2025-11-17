from django.contrib import admin
from .models import CompanyCreditProfile

@admin.register(CompanyCreditProfile)
class CompanyCreditProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'created_at', 'status', 'score', 'model_version')
    search_fields = ('company_name', 'tax_id')