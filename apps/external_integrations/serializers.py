from rest_framework import serializers
from .models import SoliqRecord, KadastrRecord

class SoliqRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=SoliqRecord
        fields=('id', 'inn', 'name', 'data', 'fetched_at')
        read_only_fields=('id', 'data', 'fetched_at')


class KadastrRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=KadastrRecord
        fields=('id', 'parcel_id', 'owner_name', 'address', 'data', 'fetched_at')
        read_only_fields=('id', 'data', 'fetched_at')