"""
Scoring engine with:
- optional joblib model loader (if model files exist)
- deterministic rule-based fallbacks for both individuals and companies
Exports:
- predict_individual_risk(features) -> (score:int, explanation:list, model_version:str)
- predict_company_risk(features)    -> (score:int, explanation:list, model_version:str)
"""
import os
from typing import Dict, Any, List, Tuple

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
INDIVIDUAL_MODEL_PATH = os.path.join(MODEL_DIR, "individual_model.joblib")
COMPANY_MODEL_PATH = os.path.join(MODEL_DIR, "company_model.joblib")

try:
    import joblib
except Exception:
    joblib = None

def _load_model(path):
    if joblib is None:
        return None
    if os.path.exists(path):
        try:
            return joblib.load(path)
        except Exception:
            return None
    return None

_individual_model = _load_model(INDIVIDUAL_MODEL_PATH)
_company_model = _load_model(COMPANY_MODEL_PATH)

def _clamp_score(v):
    return max(0, min(100, int(round(v))))

def _safe_div(a, b):
    try:
        return a / b if b else None
    except Exception:
        return None

def _map_individual_features_to_vector(features: Dict[str, Any]) -> List[float]:
    income = float(features.get("yearly_income") or 0.0)
    debt = float(features.get("existing_debt") or 0.0)
    requested = float(features.get("requested_amount") or 0.0)
    collateral = float(features.get("collateral_value") or 0.0)
    credit_score = float(features.get("credit_history_score") or 0.0)
    criminal = 1.0 if features.get("criminal_history", False) else 0.0
    dti = _safe_div(debt, income) or 0.0
    col_req = _safe_div(collateral, requested) or 0.0
    return [income, debt, requested, collateral, credit_score, criminal, dti, col_req]

def _explain_rule_based_individual(features: Dict[str, Any]) -> Tuple[int, List[Dict[str, Any]]]:
    base = 50.0
    explanations: List[Dict[str, Any]] = []
    income = float(features.get("yearly_income") or 0.0)
    debt = float(features.get("existing_debt") or 0.0)
    requested = float(features.get("requested_amount") or 0.0)
    collateral = float(features.get("collateral_value") or 0.0)
    credit_score = features.get("credit_history_score")
    criminal = features.get("criminal_history", False)

    dti = _safe_div(debt, income)
    if dti is not None:
        if dti < 0.2:
            impact, reason = +12, f"dti={dti:.2f} very low"
        elif dti < 0.5:
            impact, reason = +3, f"dti={dti:.2f} moderate"
        elif dti < 1.0:
            impact, reason = -10, f"dti={dti:.2f} high"
        else:
            impact, reason = -25, f"dti={dti:.2f} very high"
        base += impact
        explanations.append({"feature": "debt_to_income", "impact": impact, "reason": reason})
    else:
        explanations.append({"feature": "debt_to_income", "impact": 0, "reason": "income or debt missing"})

    col_req = _safe_div(collateral, requested)
    if col_req is not None and requested > 0:
        if col_req >= 1.0:
            impact, reason = +10, f"collateral covers request (ratio={col_req:.2f})"
        elif col_req >= 0.5:
            impact, reason = +4, f"partial collateral (ratio={col_req:.2f})"
        else:
            impact, reason = -5, f"low collateral (ratio={col_req:.2f})"
        base += impact
        explanations.append({"feature": "collateral_to_requested", "impact": impact, "reason": reason})
    else:
        explanations.append({"feature": "collateral_to_requested", "impact": 0, "reason": "requested or collateral missing"})

    if credit_score is not None:
        try:
            cs = int(credit_score)
        except Exception:
            cs = None
        if cs is not None:
            if cs >= 700:
                impact, reason = +10, f"credit_score={cs} excellent"
            elif cs >= 500:
                impact, reason = +2, f"credit_score={cs} fair"
            else:
                impact, reason = -12, f"credit_score={cs} poor"
            base += impact
            explanations.append({"feature": "credit_history_score", "impact": impact, "reason": reason})

    if criminal:
        base -= 40
        explanations.append({"feature": "criminal_history", "impact": -40, "reason": "criminal history present"})

    return _clamp_score(base), explanations

def predict_individual_risk(features: Dict[str, Any]) -> Tuple[int, List[Dict[str, Any]], str]:
    # Normalize input keys and defaults
    data = {
        "yearly_income": features.get("yearly_income") if isinstance(features, dict) else None,
        "existing_debt": features.get("existing_debt") if isinstance(features, dict) else None,
        "requested_amount": features.get("requested_amount") if isinstance(features, dict) else None,
        "collateral_value": features.get("collateral_value") if isinstance(features, dict) else None,
        "credit_history_score": features.get("credit_history_score") if isinstance(features, dict) else None,
        "criminal_history": features.get("criminal_history", False) if isinstance(features, dict) else False,
    }

    if _individual_model is not None:
        try:
            X = _map_individual_features_to_vector(data)
            if hasattr(_individual_model, "predict_proba"):
                prob = _individual_model.predict_proba([X])[0][1]
                return _clamp_score(prob * 100), [{"feature": "model", "impact": 0, "reason": "scored by ML model"}], f"joblib:{os.path.basename(INDIVIDUAL_MODEL_PATH)}"
            elif hasattr(_individual_model, "predict"):
                p = _individual_model.predict([X])[0]
                try:
                    prob = float(p)
                    return _clamp_score(prob * 100), [{"feature": "model", "impact": 0, "reason": "scored by ML model"}], f"joblib:{os.path.basename(INDIVIDUAL_MODEL_PATH)}"
                except Exception:
                    return _clamp_score(p), [{"feature": "model", "impact": 0, "reason": "scored by ML model"}], f"joblib:{os.path.basename(INDIVIDUAL_MODEL_PATH)}"
        except Exception:
            pass

    score, explanation = _explain_rule_based_individual(data)
    return score, explanation, "rule/v1"

# ---------------- company ----------------

def _map_company_features_to_vector(features: Dict[str, Any]) -> List[float]:
    revenue = float(features.get("revenue") or 0.0)
    net_income = float(features.get("net_income") or 0.0)
    assets = float(features.get("assets") or 0.0)
    liabilities = float(features.get("liabilities") or 0.0)
    profit_margin = _safe_div(net_income, revenue) or 0.0
    equity = max(0.0, assets - liabilities)
    leverage = _safe_div(liabilities, equity) or 0.0
    return [revenue, net_income, assets, liabilities, profit_margin, leverage]

def _explain_rule_based_company(features: Dict[str, Any]) -> Tuple[int, List[Dict[str, Any]]]:
    base = 50.0
    explanations: List[Dict[str, Any]] = []
    revenue = float(features.get("revenue") or 0.0)
    net_income = float(features.get("net_income") or 0.0)
    assets = float(features.get("assets") or 0.0)
    liabilities = float(features.get("liabilities") or 0.0)

    if revenue > 0:
        prof = net_income / revenue
        if prof > 0.1:
            impact, reason = +15, f"profitability={prof:.2f} good"
        elif prof > 0:
            impact, reason = +5, f"profitability={prof:.2f} low positive"
        else:
            impact, reason = -15, f"profitability={prof:.2f} negative"
        base += impact
        explanations.append({"feature": "profitability", "impact": impact, "reason": reason})
    else:
        explanations.append({"feature": "profitability", "impact": 0, "reason": "revenue missing or zero"})

    equity = max(0.0, assets - liabilities)
    if equity > 0:
        leverage = liabilities / equity if equity else float("inf")
        if leverage < 1:
            impact, reason = +10, f"leverage={leverage:.2f} low"
        elif leverage < 2:
            impact, reason = 0, f"leverage={leverage:.2f} moderate"
        else:
            impact, reason = -15, f"leverage={leverage:.2f} high"
        base += impact
        explanations.append({"feature": "leverage", "impact": impact, "reason": reason})
    else:
        explanations.append({"feature": "leverage", "impact": 0, "reason": "assets or liabilities missing"})

    return _clamp_score(base), explanations

def predict_company_risk(features: Dict[str, Any]) -> Tuple[int, List[Dict[str, Any]], str]:
    data = {
        "revenue": features.get("revenue") if isinstance(features, dict) else None,
        "net_income": features.get("net_income") if isinstance(features, dict) else None,
        "assets": features.get("assets") if isinstance(features, dict) else None,
        "liabilities": features.get("liabilities") if isinstance(features, dict) else None,
    }

    if _company_model is not None:
        try:
            X = _map_company_features_to_vector(data)
            if hasattr(_company_model, "predict_proba"):
                prob = _company_model.predict_proba([X])[0][1]
                return _clamp_score(prob * 100), [{"feature": "model", "impact": 0, "reason": "scored by ML model"}], f"joblib:{os.path.basename(COMPANY_MODEL_PATH)}"
            elif hasattr(_company_model, "predict"):
                p = _company_model.predict([X])[0]
                try:
                    prob = float(p)
                    return _clamp_score(prob * 100), [{"feature": "model", "impact": 0, "reason": "scored by ML model"}], f"joblib:{os.path.basename(COMPANY_MODEL_PATH)}"
                except Exception:
                    return _clamp_score(p), [{"feature": "model", "impact": 0, "reason": "scored by ML model"}], f"joblib:{os.path.basename(COMPANY_MODEL_PATH)}"
        except Exception:
            pass

    score, explanation = _explain_rule_based_company(data)
    return score, explanation, "rule/v1"