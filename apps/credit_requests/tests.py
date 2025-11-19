from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from apps.individuals.models import IndividualCreditProfile
from apps.companies.models import CompanyCreditProfile

class CreditRequestTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('creditrequest-list-create')

        # Create sample individual and company
        self.individual = IndividualCreditProfile.objects.create(
            full_name="Test Individual",
            yearly_income=1000000,
            existing_debt=100000,
            collateral_value=200000,
            credit_history_score=650,
            criminal_history=False
        )
        self.company = CompanyCreditProfile.objects.create(
            company_name="Test Co",
            revenue=5000000,
            net_income=200000,
            assets=10000000,
            liabilities=2000000
        )

    def test_create_individual_credit_request(self):
        payload = {
            "applicant_type": "individual",
            "individual": self.individual.id,
            "requested_amount": 200000,
            "term_months": 12
        }
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertIn('score', resp.data)
        # score should be present in DB
        self.assertIsNotNone(resp.data['score'])

    def test_create_company_credit_request(self):
        payload = {
            "applicant_type": "company",
            "company": self.company.id,
            "requested_amount": 1000000,
            "term_months": 24
        }
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertIn('score', resp.data)