from rest_framework import serializers
from .models import CompanyCreditProfile

class CompanyCreditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyCreditProfile
        fields = '__all__'
        read_only_fields = ('id', 'score', 'model_version', 'created_at', 'updated_at')


    def validate_revenue(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Revenue must be non-negative.")
        return value

    