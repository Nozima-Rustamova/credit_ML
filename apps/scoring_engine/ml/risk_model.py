def predict_individual_risk(data):
    income=data["yearly_income"]
    debt=data["existing_debt"]
    collateral=data["collateral_value"]

    debt_ratio=debt/(income+1)
    collateral_ratio=collateral/(debt+1)

    score =(debt_ratio*0.6+(1/(collateral_ratio+0.1))*0.4)*100
    explanation={
        "debt_ratio": round(debt_ratio,2),
        "collateral_ratio": round(collateral_ratio,2)
    }

    return round(score, 2), explanation


