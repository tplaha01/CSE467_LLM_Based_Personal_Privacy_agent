from . import HARMS
def score(records):
    totals={h:{"TP":0,"FP":0,"TN":0,"FN":0} for h in HARMS}; tp_total=pred_total=truth_total=0; exact=0
    for r in records:
        pred=r.get("parsed_prediction") or {}; truth=r["truth"]; matched=True
        for h in HARMS:
            y=int(truth[h]); item=pred.get(h,{}); p=int(item.get("label",0)) if isinstance(item,dict) else 0; matched &= y==p
            outcome=("TP" if y and p else "FP" if p else "FN" if y else "TN")
            totals[h][outcome]+=1; tp_total += int(y and p); pred_total += p; truth_total += y
        exact+=matched
    per=[]
    for h,x in totals.items():
        p=x["TP"]/(x["TP"]+x["FP"]) if x["TP"]+x["FP"] else 0; q=x["TP"]/(x["TP"]+x["FN"]) if x["TP"]+x["FN"] else 0
        per.append({"harm":h,**x,"precision":p,"recall":q,"f1":2*p*q/(p+q) if p+q else 0,"support":x["TP"]+x["FN"]})
    mp=sum(x["precision"] for x in per)/len(per); mr=sum(x["recall"] for x in per)/len(per); mf=sum(x["f1"] for x in per)/len(per)
    micro_p=tp_total/pred_total if pred_total else 0; micro_r=tp_total/truth_total if truth_total else 0
    return {"overall":{"micro_precision":micro_p,"micro_recall":micro_r,"micro_f1":2*micro_p*micro_r/(micro_p+micro_r) if micro_p+micro_r else 0,"macro_precision":mp,"macro_recall":mr,"macro_f1":mf,"exact_match_accuracy":exact/len(records) if records else 0,"hamming_loss":sum(x["FP"]+x["FN"] for x in totals.values())/(len(records)*len(HARMS)) if records else 0},"per_harm":per}
