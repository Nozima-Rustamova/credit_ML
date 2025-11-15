from rest_framework import serializers
from .models import IndividualCreditProfile

class IndividualCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualCreditProfile
        fields = '__all__'