from django.urls import path
from .views import PredictIndividualView, PredictCompanyView

urlpatterns = [
    path('individual/', PredictIndividualView.as_view(), name='predict-individual'),
    path('company/', PredictCompanyView.as_view(), name='predict-company'),
]
