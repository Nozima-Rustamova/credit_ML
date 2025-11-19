from django.contrib import admin
from .models import SoliqRecord, KadastrRecord

@admin.register(SoliqRecord)
class SoliqRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'inn', 'name', 'fetched_at')
    search_fields = ('inn', 'name')
    readonly_fields = ('data', 'fetched_at')

@admin.register(KadastrRecord)
class KadastrRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'parcel_id', 'owner_name', 'address', 'fetched_at')
    search_fields = ('parcel_id', 'owner_name')
    readonly_fields = ('data', 'fetched_at')