import csv, json
from pathlib import Path
from . import HARMS
def write_errors(records, path):
    rows=[]
    for r in records:
        if r.get("validation_status") != "valid":
            rows.append({"statement_id":r.get("statement_id"),"harm_category":"","error_type":"invalid output","ground_truth":"","prediction":"","model_evidence":"","raw_response":r.get("raw_model_response"),"model_id":r.get("model_id")}); continue
        for h in HARMS:
            y=int(r["truth"][h]); p=int(r["parsed_prediction"][h]["label"])
            if y != p: rows.append({"statement_id":r["statement_id"],"harm_category":h,"error_type":"false positive" if p else "false negative","ground_truth":y,"prediction":p,"model_evidence":r["parsed_prediction"][h].get("evidence"),"raw_response":r.get("raw_model_response"),"model_id":r.get("model_id")})
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["statement_id","harm_category","error_type","ground_truth","prediction","model_evidence","raw_response","model_id"]); w.writeheader(); w.writerows(rows)
