from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import PredictionLog
from .models import IndividualCreditProfile

class PredictionLogTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('individual-score')

    def test_prediction_log_created_on_individual_score(self):
        payload = {
            "full_name": "Audit User",
            "yearly_income": 1000000,
            "existing_debt": 100000,
            "collateral_value": 200000,
            "requested_amount": 150000,
            "credit_history_score": 640,
            "criminal_history": False
        }
        resp = self.client.post(self.url, payload, format='json')
        self.assertEqual(resp.status_code, 200)

        # Ensure individual was created
       