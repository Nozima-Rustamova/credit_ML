from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import SoliqRecord, KadastrRecord
from .serializers import SoliqRecordSerializer, KadastrRecordSerializer
from .clients import fetch_soliq_mock, fetch_kadastr_mock

class SoliqRetrieveView(APIView):
    """
    GET /api/external/soliq/<inn>/
    Returns stored SoliqRecord if exists, otherwise fetches mock data, stores it, and returns it.
    """
    def get(self, request, inn, *args, **kwargs):
        # try DB first
        try:
            rec = SoliqRecord.objects.filter(inn=inn).order_by("-fetched_at").first()
        except Exception:
            rec = None

        if rec:
            serializer = SoliqRecordSerializer(rec)
            return Response(serializer.data)

        # fetch mock
        data = fetch_soliq_mock(inn)
        rec = SoliqRecord.objects.create(
            inn=inn,
            name=data.get("registered_name"),
            data=data
        )
        serializer = SoliqRecordSerializer(rec)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class KadastrRetrieveView(APIView):
    """
    GET /api/external/kadastr/<parcel_id>/
    """
    def get(self, request, parcel_id, *args, **kwargs):
        rec = KadastrRecord.objects.filter(parcel_id=parcel_id).order_by("-fetched_at").first()
        if rec:
            serializer = KadastrRecordSerializer(rec)
            return Response(serializer.data)

        data = fetch_kadastr_mock(parcel_id)
        rec = KadastrRecord.objects.create(
            parcel_id=parcel_id,
            owner_name=data.get("owner_name"),
            address=data.get("address"),
            data=data
        )
        serializer = KadastrRecordSerializer(rec)
        return Response(serializer.data, status=status.HTTP_201_CREATED)