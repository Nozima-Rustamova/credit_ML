'''
Client layer that simulates calls to external goverment APIs which we dont have access yet
Replacing the fuctions here withreal HTTP calls
Keeping it modular makes swapping for real clients trivial
'''

import random
import datetime

def fetch_soliq_mock(inn: str) ->dict:
    '''
    Return deterministic-ish mock data for a given INN
    '''

    seed = sum(ord(c) for c in inn) % 1000
    rng = random.Random(seed)
    last_tax_paid = (datetime.datetime.utcnow() - datetime.timedelta(days=rng.randint(0, 1000))).isoformat()
    income_declared = rng.randint(1_000_000, 200_000_000)
    tax_paid = int(income_declared * rng.uniform(0.05, 0.2))

    data = {
        "inn": inn,
        "registered_name": f"Entity {inn[-4:]}",
        "last_tax_paid_at": last_tax_paid,
        "yearly_income_declared": income_declared,
        "total_tax_paid": tax_paid,
        "tax_clear": rng.choice([True, True, True, False]),  # mostly clear
        "raw": {
            "note": "This is mock Soliq data for development only."
        }
    }
    return data


def fetch_kadastr_mock(parcel_id: str) -> dict:
    """
    Return deterministic-ish mock cadastral record for a parcel ID.
    """
    seed = sum(ord(c) for c in parcel_id) % 1000
    rng = random.Random(seed)
    owner = f"Owner {parcel_id[-4:]}"
    address = f"{rng.randint(1,200)} Example St, Tashkent"
    area_sq_m = rng.randint(100, 2000)

    data = {
        "parcel_id": parcel_id,
        "owner_name": owner,
        "address": address,
        "area_sqm": area_sq_m,
        "usage": rng.choice(["residential", "agricultural", "commercial"]),
        "raw": {
            "note": "Mock Kadastr record."
        }
    }
    return data