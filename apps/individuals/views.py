from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import OperationalError

from .models import IndividualCreditProfile
from .serializers import IndividualCreditSerializer

from apps.scoring_engine.ml.risk_model import predict_individual_risk

class IndividualCreditView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = IndividualCreditSerializer(data=request.data)
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
            application.score = int(score)
            application.model_version = model_version
            application.save(update_fields=['score', 'model_version', 'updated_at'])
        except Exception:
            # non-fatal for endpoint: we still return the score even if DB update fails
            pass

            return Response({
                "id": application.id,
                "risk_score": score,
                "explanation": explanation,
                "model_version": model_version,
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            