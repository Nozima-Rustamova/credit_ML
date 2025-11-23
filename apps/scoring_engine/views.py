from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .ml.risk_model import predict_individual_risk, predict_company_risk


class PredictIndividualView(APIView):
    """POST /api/score/individual/ - accepts JSON features and returns score + explanation"""
    def post(self, request, *args, **kwargs):
        features = request.data if isinstance(request.data, dict) else {}
        score, explanation, model_ver = predict_individual_risk(features)
        return Response({"score": int(score) if score is not None else None, "explanation": explanation, "model_version": model_ver})


class PredictCompanyView(APIView):
    """POST /api/score/company/ - accepts JSON features and returns score + explanation"""
    def post(self, request, *args, **kwargs):
        features = request.data if isinstance(request.data, dict) else {}
        score, explanation, model_ver = predict_company_risk(features)
        return Response({"score": int(score) if score is not None else None, "explanation": explanation, "model_version": model_ver})
