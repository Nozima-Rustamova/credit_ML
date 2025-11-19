from django.db import OperationalError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import IndividualCreditProfileSerializer
from .models import IndividualCreditProfile, PredictionLog
from apps.scoring_engine.ml.risk_model import predict_individual_risk

class IndividualCreditView(APIView):
    """
    POST /api/individuals/score/
    Validates, saves application, runs scoring, updates the instance with score & model_version, returns result.
    """
    def post(self, request, *args, **kwargs):
        serializer = IndividualCreditProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            application = serializer.save()
        except OperationalError as exc:
            # DB might not be migrated yet
            return Response(
                {"detail": "Database error while saving application. Run migrations. Error: " + str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Build features dict for scoring - prefer validated_data
        features = serializer.validated_data
        score, explanation, model_version = predict_individual_risk(features)

        # Save score and model_version without re-validating everything
        try:
            application.score = int(score) if score is not None else None
            application.model_version = model_version
            application.explanation = explanation
            application.save(update_fields=['score', 'model_version', 'explanation', 'updated_at'])
        except Exception:
            # non-fatal for endpoint: we still return the score even if DB update fails
            pass

        # Create an audit log entry
        try:
            PredictionLog.objects.create(
                profile=application,
                score=int(score) if score is not None else None,
                model_version=model_version,
                explanation=explanation,
                meta={
                    "request_ip": request.META.get("REMOTE_ADDR"),
                    "user_agent": request.META.get("HTTP_USER_AGENT"),
                    "raw_features": features
                }
            )
        except Exception:
            # logging failure must not break API response
            pass

        return Response({
            "id": application.id,
            "score": score,
            "explanation": explanation,
            "model_version": model_version
        }, status=status.HTTP_200_OK)