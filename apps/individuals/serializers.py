from rest_framework import serializers
from .models import IndividualCreditProfile, PredictionLog

class IndividualCreditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualCreditProfile
        fields = '__all__'
        read_only_fields = ('id', 'status', 'score', 'model_version', 'created_at', 'updated_at', 'explanation')

class PredictionLogSerializer(serializers.ModelSerializer):
    # convenience fields to surface the attached object
    content_type = serializers.CharField(source='content_type.model', read_only=True)
    object_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PredictionLog
        fields = ('id', 'content_type', 'object_id', 'score', 'model_version', 'explanation', 'features', 'created_at')
        read_only_fields = ('id', 'content_type', 'object_id', 'score', 'model_version', 'explanation', 'features', 'created_at')