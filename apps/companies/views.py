from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import OperationalError

from .serializers import CompanyCreditProfileSerializer
from .models import CompanyCreditProfile
from apps.scoring_engine.ml.risk_model import predict_company_risk  

class CompanyCreditView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CompanyCreditProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            application = serializer.save()
        except OperationalError as exc:
            return Response(
                {"detail": "Database error while saving application. Error: " + str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        features = serializer.validated_data
        score, explanation, model_version = predict_company_risk(features)

        try:
            application.score = int(score)
            application.model_version = model_version
            application.save(update_fields=['score', 'model_version', 'updated_at'])
        except Exception:
            pass

        return Response({
            "id": application.id,
            "score": score,
            "explanation": explanation,
            "model_version": model_version
        }, status=status.HTTP_200_OK) 