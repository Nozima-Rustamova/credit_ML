# tasks/tasks.py
import logging
from datetime import timedelta, datetime

from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)

# Import models/clients inside tasks so Django has been configured before imports
@shared_task(bind=True)
def refresh_soliq_record(self, inn: str) -> dict:
    """
    Fetch (mock) Soliq record for the given INN and persist/update the DB record.
    Returns the record data or {} on failure.
    """
    try:
        from apps.external_integrations.clients import fetch_soliq_mock
        from apps.external_integrations.models import SoliqRecord
    except Exception as exc:
        logger.exception("Missing external_integrations app or imports: %s", exc)
        return {}

    try:
        data = fetch_soliq_mock(inn)
        rec, created = SoliqRecord.objects.update_or_create(
            inn=inn,
            defaults={"name": data.get("registered_name"), "data": data},
        )
        logger.info("Soliq record refreshed for %s (created=%s)", inn, created)
        return data
    except Exception:
        logger.exception("Failed to refresh Soliq for %s", inn)
        return {}


@shared_task(bind=True)
def refresh_kadastr_record(self, parcel_id: str) -> dict:
    """
    Fetch (mock) Kadastr record for the given parcel id and persist/update the DB record.
    """
    try:
        from apps.external_integrations.clients import fetch_kadastr_mock
        from apps.external_integrations.models import KadastrRecord
    except Exception as exc:
        logger.exception("Missing external_integrations app or imports: %s", exc)
        return {}

    try:
        data = fetch_kadastr_mock(parcel_id)
        rec, created = KadastrRecord.objects.update_or_create(
            parcel_id=parcel_id,
            defaults={"owner_name": data.get("owner_name"), "address": data.get("address"), "data": data},
        )
        logger.info("Kadastr record refreshed for %s (created=%s)", parcel_id, created)
        return data
    except Exception:
        logger.exception("Failed to refresh Kadastr for %s", parcel_id)
        return {}


@shared_task(bind=True)
def refresh_stale_external_records(self, ttl_days: int = 30):
    """
    Find stored external records older than ttl_days and refresh them.
    This task iterates both SoliqRecord and KadastrRecord tables.
    """
    try:
        from apps.external_integrations.models import SoliqRecord, KadastrRecord
    except Exception as exc:
        logger.exception("Missing external_integrations models: %s", exc)
        return

    cutoff = timezone.now() - timedelta(days=ttl_days)

    # Soliq
    stale_soliq = SoliqRecord.objects.filter(fetched_at__lt=cutoff)
    for rec in stale_soliq:
        try:
            refresh_soliq_record.delay(rec.inn)
        except Exception:
            logger.exception("Failed to schedule refresh_soliq_record for %s", rec.inn)

    # Kadastr
    stale_kadastr = KadastrRecord.objects.filter(fetched_at__lt=cutoff)
    for rec in stale_kadastr:
        try:
            refresh_kadastr_record.delay(rec.parcel_id)
        except Exception:
            logger.exception("Failed to schedule refresh_kadastr_record for %s", rec.parcel_id)


@shared_task(bind=True)
def rescore_pending_credit_requests(self, limit: int = 100):
    """
    Recompute scores for recent (pending) credit requests that don't have scores or whose status is pending.
    Limit controls how many are processed per run to avoid long tasks.
    """
    try:
        from apps.credit_requests.models import CreditRequest
        from apps.scoring_engine.ml.risk_model import predict_individual_risk, predict_company_risk
        from apps.individuals.models import PredictionLog
    except Exception as exc:
        logger.exception("Missing apps: %s", exc)
        return

    qs = CreditRequest.objects.filter(status=CreditRequest.STATUS_PENDING).order_by("created_at")[:limit]
    logger.info("Rescoring %d pending credit requests", qs.count())

    for cr in qs:
        try:
            if cr.applicant_type == CreditRequest.APPLICANT_INDIVIDUAL and cr.individual:
                p = cr.individual
                features = {
                    "yearly_income": p.yearly_income,
                    "existing_debt": p.existing_debt,
                    "requested_amount": cr.requested_amount,
                    "collateral_value": p.collateral_value,
                    "credit_history_score": p.credit_history_score,
                    "criminal_history": p.criminal_history,
                }
                score, explanation, model_ver = predict_individual_risk(features)
            elif cr.applicant_type == CreditRequest.APPLICANT_COMPANY and cr.company:
                c = cr.company
                features = {
                    "revenue": c.revenue,
                    "net_income": c.net_income,
                    "assets": c.assets,
                    "liabilities": c.liabilities,
                    "requested_amount": cr.requested_amount,
                }
                score, explanation, model_ver = predict_company_risk(features)
            else:
                continue

            cr.score = int(score) if score is not None else None
            cr.model_version = model_ver
            cr.explanation = explanation
            cr.updated_at = timezone.now()
            cr.save(update_fields=["score", "model_version", "explanation", "updated_at"])

            # log prediction
            try:
                PredictionLog.objects.create(
                    content_object=cr,
                    score=int(score) if score is not None else None,
                    model_version=model_ver,
                    explanation=explanation,
                    features=features,
                )
            except Exception:
                logger.exception("Failed to create PredictionLog for CreditRequest %s", cr.id)
        except Exception:
            logger.exception("Failed to rescore CreditRequest %s", cr.id)


@shared_task(bind=True)
def cleanup_prediction_logs(self, older_than_days: int = 90) -> int:
    """
    Delete PredictionLog entries older than `older_than_days`.
    Returns the count of deleted entries.
    """
    try:
        from apps.individuals.models import PredictionLog
    except Exception as exc:
        logger.exception("Missing PredictionLog model: %s", exc)
        return 0

    cutoff = timezone.now() - timedelta(days=older_than_days)
    qs = PredictionLog.objects.filter(created_at__lt=cutoff)
    count = qs.count()
    qs.delete()
    logger.info("Deleted %d prediction logs older than %d days", count, older_than_days)
    return count