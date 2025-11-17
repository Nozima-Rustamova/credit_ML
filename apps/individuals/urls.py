from django.urls import path
from .views import IndividualCreditView

urlpatterns = [
    path('score/', IndividualCreditView.as_view(), name='individual-score'),
]
