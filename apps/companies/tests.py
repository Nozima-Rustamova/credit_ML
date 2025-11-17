from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

class CompanyEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('company-score')

    def test_post_valid_company(self):
        payload = {
            "company_name": "Acme LLC",
            "revenue": 100000000,
            "net_income": 5000000,
            "assets": 200000000,
            "liabilities": 50000000
        }
        resp = self.client.post(self.url, payload, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn("score", resp.data)