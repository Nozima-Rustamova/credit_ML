from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import CreditRequest
from .serializers import CreditRequestSerializer

# scoring functions
from apps.scoring_engine.ml.risk_model import predict_individual_risk, predict_company_risk

# Import PredictionLog to persist audit entries for credit requests
from apps.individuals.models import PredictionLog

class CreditRequestListCreateView(generics.ListCreateAPIView):
    queryset = CreditRequest.objects.all()
    serializer_class = CreditRequestSerializer

    def perform_create(self, serializer):
        # Save initial record first (will be status=pending)
        instance = serializer.save()

        # Build features from linked profile and request fields
        try:
            if instance.applicant_type == CreditRequest.APPLICANT_INDIVIDUAL and instance.individual:
                p = instance.individual
                features = {
                    "yearly_income": p.yearly_income,
                    "existing_debt": p.existing_debt,
                    "requested_amount": instance.requested_amount,
                    "collateral_value": p.collateral_value,
                    "credit_history_score": p.credit_history_score,
                    "criminal_history": p.criminal_history,
                }
                score, explanation, model_ver = predict_individual_risk(features)
            elif instance.applicant_type == CreditRequest.APPLICANT_COMPANY and instance.company:
                c = instance.company
                features = {
                    "revenue": c.revenue,
                    "net_income": c.net_income,
                    "assets": c.assets,
                    "liabilities": c.liabilities,
                    "requested_amount": instance.requested_amount,
                }
                score, explanation, model_ver = predict_company_risk(features)
            else:
                # nothing to score
                score, explanation, model_ver = None, None, None
        except Exception as exc:
            # Do not block creation if scoring fails, but log/store nulls
            score, explanation, model_ver = None, None, None

        if score is not None:
            instance.score = int(score)
            instance.model_version = model_ver
            instance.explanation = explanation
            instance.save(update_fields=['score', 'model_version', 'explanation', 'updated_at'])

            # create an audit log entry referencing the credit request (and profile if available)
            try:
                PredictionLog.objects.create(
                    profile=instance.individual if instance.individual_id else None,
                    credit_request=instance,
                    score=int(score),
                    model_version=model_ver,
                    explanation=explanation,
                    meta={
                        "requested_amount": instance.requested_amount,
                        "term_months": instance.term_months
                    }
                )
            except Exception:
                pass

class CreditRequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = CreditRequest.objects.all()
    serializer_class = CreditRequestSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        # Optionally re-score on update if applicant_type or amounts changed.
        try:
            if instance.applicant_type == CreditRequest.APPLICANT_INDIVIDUAL and instance.individual:
                p = instance.individual
                features = {
                    "yearly_income": p.yearly_income,
                    "existing_debt": p.existing_debt,
                    "requested_amount": instance.requested_amount,
                    "collateral_value": p.collateral_value,
                    "credit_history_score": p.credit_history_score,
                    "criminal_history": p.criminal_history,
                }
                score, explanation, model_ver = predict_individual_risk(features)
            elif instance.applicant_type == CreditRequest.APPLICANT_COMPANY and instance.company:
                c = instance.company
                features = {
                    "revenue": c.revenue,
                    "net_income": c.net_income,
                    "assets": c.assets,
                    "liabilities": c.liabilities,
                    "requested_amount": instance.requested_amount,
                }
                score, explanation, model_ver = predict_company_risk(features)
            else:
                score, explanation, model_ver = None, None, None
        except Exception:
            score, explanation, model_ver = None, None, None

        if score is not None:
            instance.score = int(score)
            instance.model_version = model_ver
            instance.explanation = explanation
            instance.save(update_fields=['score', 'model_version', 'explanation', 'updated_at'])

            try:
                PredictionLog.objects.create(
                    profile=instance.individual if instance.individual_id else None,
                    credit_request=instance,
                    score=int(score),
                    model_version=model_ver,
                    explanation=explanation,
                    meta={"updated_via": "credit_request_update"}
                )
            except Exception:
                pass