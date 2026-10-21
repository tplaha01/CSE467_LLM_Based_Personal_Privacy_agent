import json, re
from pathlib import Path
from . import HARMS

def validate_prediction(value, schema_path="schemas/prediction.schema.json"):
    errors=[]
    if not isinstance(value, dict) or set(value) != set(HARMS): return False, ["exact harm keys required"]
    for h in HARMS:
        item=value[h]
        if not isinstance(item, dict) or set(item) != {"label","evidence"}: errors.append(f"{h}: fields") ; continue
        if item["label"] not in (0,1): errors.append(f"{h}: label")
        if item["label"] == 0 and item["evidence"] is not None: errors.append(f"{h}: evidence must be null for 0")
        if item["label"] == 1 and not isinstance(item["evidence"], str): errors.append(f"{h}: evidence required for 1")
    return not errors, errors

def parse_and_validate(raw):
    try:
        text=raw.strip(); text=re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I)
        value=json.loads(text)
    except Exception as e: return None, False, [f"invalid JSON: {e}"]
    ok, errors=validate_prediction(value); return value if ok else value, ok, errors

def evidence_present(evidence, statement):
    if evidence is None: return None
    norm=lambda s: " ".join(str(s).split()).lower()
    return norm(evidence) in norm(statement)
