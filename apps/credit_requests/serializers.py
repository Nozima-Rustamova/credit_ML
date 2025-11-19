from rest_framework import serializers
from .models import CreditRequest
from apps.individuals.models import IndividualCreditProfile
from apps.companies.models import CompanyCreditProfile

class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=CreditRequest
        fields='__all__'
        read_only_fields=('id', 'score', 'model_version', 'explanation', 'created_at', 'updated_at')

    def validate(self, data):
        applicant_type = data.get('applicant_type') or getattr(self.instance, 'applicant_type', None)
        individual = data.get('individual') if 'individual' in data else getattr(self.instance, 'individual', None)
        company = data.get('company') if 'company' in data else getattr(self.instance, 'company', None)

        if applicant_type == CreditRequest.APPLICANT_INDIVIDUAL:
            if not individual:
                raise serializers.ValidationError({"individual": "This field is required for applicant_type 'individual'."})
            # ensure provided object is correct type
            if not isinstance(individual, IndividualCreditProfile):
                raise serializers.ValidationError({"individual": "Invalid individual reference."})
            # force company to be null
            if company:
                raise serializers.ValidationError({"company": "Must be empty when applicant_type is 'individual'."})
        elif applicant_type == CreditRequest.APPLICANT_COMPANY:
            if not company:
                raise serializers.ValidationError({"company": "This field is required for applicant_type 'company'."})
            if not isinstance(company, CompanyCreditProfile):
                raise serializers.ValidationError({"company": "Invalid company reference."})
            if individual:
                raise serializers.ValidationError({"individual": "Must be empty when applicant_type is 'company'."})
        else:
            raise serializers.ValidationError({"applicant_type": "Invalid applicant_type. Choose 'individual' or 'company'."})

        # requested_amount sanity
        req_amt = data.get('requested_amount') or getattr(self.instance, 'requested_amount', None)
        if req_amt is None or req_amt <= 0:
            raise serializers.ValidationError({"requested_amount": "requested_amount must be > 0."})

        return data