import csv
from pathlib import Path
from . import HARMS

def _read(path):
    with open(path, encoding="utf-8", newline="") as f: return list(csv.DictReader(f))

def validate_rows(rows, require_labels=False):
    required = ["statement_id", "statement"] + (list(HARMS) if require_labels else [])
    if not rows: raise ValueError("dataset is empty")
    missing = [x for x in required if x not in rows[0]]
    if missing: raise ValueError(f"missing columns: {missing}")
    ids = [r["statement_id"] for r in rows]
    if any(not x.strip() for x in ids): raise ValueError("missing statement IDs")
    if len(ids) != len(set(ids)): raise ValueError("duplicate statement IDs")
    if any(not r["statement"].strip() for r in rows): raise ValueError("missing statements")
    if require_labels:
        for r in rows:
            for h in HARMS:
                if r[h] not in {"0", "1"}: raise ValueError(f"invalid label for {r['statement_id']}/{h}: {r[h]}")
    statements = [r["statement"] for r in rows]
    if len(statements) != len(set(statements)): raise ValueError("duplicate statements")
    return rows

def load_statements(path):
    return [{"statement_id": r["statement_id"], "statement": r["statement"]} for r in validate_rows(_read(path), False)]

def load_ground_truth(path): return validate_rows(_read(path), True)
