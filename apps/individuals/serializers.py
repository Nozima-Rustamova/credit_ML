from rest_framework import serializers
from .models import IndividualCreditProfile

class IndividualCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualCreditProfile
        fields = '__all__'
        read_only_fields=('id', 'status', 'score', 'model_version', 'created_at', 'updated_at')

        def validate_yearly_income(self, value):
            if value is not None and value < 0:
                raise serializers.ValidationError("Yearly income must be non-negative.")
            return value
        
        def validate_existing_debt(self, value):
            if value is not None and value < 0:
                raise serializers.ValidationError("Existing debt must be non-negative.")
            return value
        
        def validate_requested_amount(self, value):
            if value is not None and value <= 0:
                raise serializers.ValidationError("Requested amount must be positive.")
            return value
        
        def validate_term_months(self, value):
            if value is not None and value <= 0:
                raise serializers.ValidationError("Term months must be positive.")
            return value