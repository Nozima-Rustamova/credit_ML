from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import IndividualCreditProfile
from .serializers import IndividualCreditSerializer

from apps.scoring_engine.ml.risk_model import predict_individual_risk

class IndividualCreditView(APIView):
    def post(self, request):
        serializer = IndividualCreditSerializer(data=request.data)
        if serializer.is_valid():
            application=serializer.save()

            #ml prediction
            score, explanation = predict_individual_risk(serializer.validated_data)

            application.risk_score=score
            application.explanation=explanation
            application.save()

            return Response({
                "id": application.id,
                "risk_score": score,
                "explanation": explanation
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            