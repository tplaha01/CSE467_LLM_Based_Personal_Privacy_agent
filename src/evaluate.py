import argparse,csv,json
from pathlib import Path
from .dataset import load_ground_truth
from .metrics import score
from .error_analysis import write_errors
from . import HARMS
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--run",required=True); ap.add_argument("--dataset",default="data/ground_truth.csv"); ap.add_argument("--result-dir",default="results"); a=ap.parse_args()
    gt={r["statement_id"]:r for r in load_ground_truth(a.dataset)}; records=[]
    for line in (Path("predictions")/a.run/"run.jsonl").read_text(encoding="utf-8").splitlines():
        r=json.loads(line)
        if r["statement_id"] in gt: r["truth"]=gt[r["statement_id"]]; records.append(r)
    metrics=score(records); out=Path(a.result_dir)/a.run; out.mkdir(parents=True,exist_ok=True)
    (out/"metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    with (out/"predictions_with_ground_truth.csv").open("w",newline="",encoding="utf-8") as f:
        fields=["statement_id"]+list(HARMS)+[f"pred_{h}" for h in HARMS]; w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in records:
            pred=r.get("parsed_prediction") or {}
            w.writerow({"statement_id":r["statement_id"],**{h:r["truth"][h] for h in HARMS},**{f"pred_{h}":(pred.get(h,{}).get("label","") if isinstance(pred.get(h,{}),dict) else "") for h in HARMS}})
    write_errors(records,out/"errors.csv")
    for name, rows in (("overall_metrics.csv",[metrics["overall"]]),("per_harm_metrics.csv",metrics["per_harm"])):
        with (out/name).open("w",newline="",encoding="utf-8") as f: w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(json.dumps(metrics["overall"],indent=2))
if __name__=="__main__": main()
