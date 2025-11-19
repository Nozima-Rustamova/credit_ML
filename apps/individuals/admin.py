from django.contrib import admin
from .models import IndividualCreditProfile, PredictionLog

@admin.register(IndividualCreditProfile)
class IndividualCreditProfileAdmin(admin.ModelAdmin):
    list_display=('id', 'full_name', 'created_at', 'status', 'score', 'model_version')
    list_filter=('status', 'created_at', 'criminal_history')
    search_fields=('full_name', 'email', 'phone')


@admin.register(PredictionLog)
class PredictionLogAdmin(admin.ModelAdmin):
     list_display = ('id', 'profile', 'credit_request', 'score', 'model_version', 'created_at')
     readonly_fields = ('explanation', 'meta', 'created_at')
     search_fields = ('profile__full_name', 'credit_request__id', 'model_version')
     list_filter = ('model_version',)