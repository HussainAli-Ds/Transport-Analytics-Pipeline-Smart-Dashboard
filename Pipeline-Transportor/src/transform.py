import pandas as pd
import re
from thefuzz import process
from config import (
    KNOWN_TRANSPORTERS,
    KNOWN_MATERIALS,
    TRANSPORTER_ALIASES,
    MATERIAL_ALIASES,
    FUZZ_THRESHOLD
)

def normalize_text(value):
    if not value:
        return ""
    value = str(value).lower().strip()
    value = re.sub(r"[^a-z0-9\s]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value


def smart_match(value, choices, aliases):
    clean_val = normalize_text(value)

    if clean_val in aliases:
        return aliases[clean_val]

    result = process.extractOne(clean_val, choices)
    if result:
        match, score = result
        if score >= FUZZ_THRESHOLD:
            return match

    return None


def clean_data(df):

    df = df.rename(columns={
        "transportor": "transporter",
        "from": "from_location",
        "to": "to_location"
    })

    cols = [
        "dated", "transporter", "vehicle_no", "material",
        "zkb_slip_no", "supplier_slip_no", "location",
        "from_location", "to_location", "trips",
        "zkb_qty_cft", "tons"
    ]

    df = df.reindex(columns=cols)

    df["transporter"] = df["transporter"].apply(
        lambda x: smart_match(x, KNOWN_TRANSPORTERS, TRANSPORTER_ALIASES)
    )

    df["material"] = df["material"].apply(
        lambda x: smart_match(x, KNOWN_MATERIALS, MATERIAL_ALIASES)
    )

    df = df[
        df["transporter"].notna() &
        df["material"].notna() &
        df["vehicle_no"].notna()
    ].copy()

    df = df.fillna({
        "zkb_slip_no": 0,
        "supplier_slip_no": 0,
        "location": "-",
        "from_location": "-",
        "to_location": "-"
    })

    df["supplier_slip_no"] = pd.to_numeric(df["supplier_slip_no"], errors="coerce").fillna(0).astype(int)
    df["zkb_slip_no"] = pd.to_numeric(df["zkb_slip_no"], errors="coerce").fillna(0).astype(int)
    df["trips"] = pd.to_numeric(df["trips"], errors="coerce").fillna(0).astype(int)
    df["zkb_qty_cft"] = pd.to_numeric(df["zkb_qty_cft"], errors="coerce").fillna(0).astype(int)
    df["tons"] = pd.to_numeric(df["tons"], errors="coerce").fillna(0).astype(float)

    df["vehicle_no"] = df["vehicle_no"].astype(str).str.strip()

    return df