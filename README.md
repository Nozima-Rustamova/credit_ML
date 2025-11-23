# credit_ML

Lightweight Django project for credit scoring prototypes. It contains:

- Mocked external integrations (Soliq, Kadastr).
- Models for individuals, companies and credit requests.
- A scoring engine with rule-based fallbacks and optional joblib model loading.
- Celery tasks for refreshing external records and rescoring credit requests.

## Quickstart

Prerequisites           

- Python 3.11+ (project created with Python 3.13 in dev environment)
- Virtual environment (recommended)

Install dependencies and activate the venv (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

Run the development server:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Run tests (example: external integrations app):

```powershell
.\.venv\Scripts\python.exe manage.py test apps.external_integrations.tests --verbosity=2
```

## API Endpoints (available / inspected)

- GET `/api/external/soliq/<inn>/` (name: `external-soliq`)
  - Returns existing `SoliqRecord` for `inn`, or fetches mock data, persists it, and returns (201 on create).

- GET `/api/external/kadastr/<parcel_id>/` (name: `external-kadastr`)
  - Same behavior for cadastral records.

Note: other apps (`individuals`, `companies`, `credit_requests`) contain models for profiles and requests — there may be additional API views or serializers (not enumerated here).

## Scoring Engine

Location: `apps/scoring_engine/ml/risk_model.py`

Exports:
- `predict_individual_risk(features: dict) -> (score:int, explanation:list, model_version:str)`
- `predict_company_risk(features: dict) -> (score:int, explanation:list, model_version:str)`

Behavior:
- If joblib model files are present in `apps/scoring_engine/ml/models/` (`individual_model.joblib`, `company_model.joblib`), they will be used.
- Otherwise the module uses deterministic, explainable rule-based scoring (useful for development and fallback).

Programmatic example:

```python
from apps.scoring_engine.ml.risk_model import predict_individual_risk
features = {
    "yearly_income": 50000,
    "existing_debt": 5000,
    "requested_amount": 10000,
    "credit_history_score": 650,
}
score, explanation, model_ver = predict_individual_risk(features)
print(score, model_ver)
```

## Background tasks (Celery)

Location: `tasks/tasks.py`

Provided tasks (shared_task):
- `refresh_soliq_record(inn)` — fetch mock Soliq and persist/update DB.
- `refresh_kadastr_record(parcel_id)` — fetch mock Kadastr and persist/update DB.
- `refresh_stale_external_records(ttl_days=30)` — finds stale records and enqueues refresh tasks.
- `rescore_pending_credit_requests(limit=100)` — recomputes scores for pending credit requests and saves results.
- `cleanup_prediction_logs(older_than_days=90)` — deletes old prediction logs.

Notes:
- The tasks are wired to use the mock clients in `apps.external_integrations.clients`. To run tasks you need a running Celery worker and broker (e.g., Redis).

## Tests

- Run targeted app tests as shown above.
- The external integrations tests are fast and pass in the project environment (they use mocks and the test DB).

## Developer notes & TODOs

- Add trained joblib models to `apps/scoring_engine/ml/models/` to enable ML scoring.
- Review `tasks/tasks.py` PredictionLog creation: the currently used field names in task code may not match the `PredictionLog` model fields exactly — consider harmonizing the task logging code with the model.
- Consider adding DRF view endpoints to expose the scoring API (POST request accepting features and returning score + explanation) and API authentication.

## License

This repository currently does not include an explicit license file. Add `LICENSE` if you plan to publish.

----

Created/updated README by developer request. For more help, tell me what part you'd like to improve next (docs, API, tasks, models or tests).
its ml model that outputs risk of giving credit
