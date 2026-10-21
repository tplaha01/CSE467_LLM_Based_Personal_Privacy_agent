from . import HARMS
def score(records):
    totals={h:{"TP":0,"FP":0,"TN":0,"FN":0} for h in HARMS}; all_t=all_p=0; exact=0
    for r in records:
        pred=r.get("parsed_prediction") or {}; truth=r["truth"]; matched=True
        for h in HARMS:
            y=int(truth[h]); p=int(pred.get(h,{}).get("label",0)); matched &= y==p
            totals[h][("TP" if y and p else "FP" if p else "FN" if y else "TN")]+=1; all_t+=y; all_p+=p
        exact+=matched
    per=[]
    for h,x in totals.items():
        p=x["TP"]/(x["TP"]+x["FP"]) if x["TP"]+x["FP"] else 0; q=x["TP"]/(x["TP"]+x["FN"]) if x["TP"]+x["FN"] else 0
        per.append({"harm":h,**x,"precision":p,"recall":q,"f1":2*p*q/(p+q) if p+q else 0,"support":x["TP"]+x["FN"]})
    mp=sum(x["precision"] for x in per)/len(per); mr=sum(x["recall"] for x in per)/len(per); mf=sum(x["f1"] for x in per)/len(per)
    micro_p=all_t/all_p if all_p else 0; micro_r=all_t/sum(x["TP"]+x["FN"] for x in totals.values()) if totals else 0
    return {"overall":{"micro_precision":micro_p,"micro_recall":micro_r,"micro_f1":2*micro_p*micro_r/(micro_p+micro_r) if micro_p+micro_r else 0,"macro_precision":mp,"macro_recall":mr,"macro_f1":mf,"exact_match_accuracy":exact/len(records) if records else 0,"hamming_loss":sum(x["FP"]+x["FN"] for x in totals.values())/(len(records)*len(HARMS)) if records else 0},"per_harm":per}
