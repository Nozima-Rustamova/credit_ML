from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from .models import SoliqRecord, KadastrRecord

class ExternalIntegrationsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_soliq_fetch_and_store(self):
        inn = "123456789"
        url = reverse('external-soliq', args=[inn])
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (200, 201))
        # record should exist now
        self.assertTrue(SoliqRecord.objects.filter(inn=inn).exists())

    def test_kadastr_fetch_and_store(self):
        parcel = "UZ-ABC-100"
        url = reverse('external-kadastr', args=[parcel])
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (200, 201))
        self.assertTrue(KadastrRecord.objects.filter(parcel_id=parcel).exists())