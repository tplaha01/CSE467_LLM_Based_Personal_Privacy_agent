import json
from pathlib import Path
import pytest
from src.dataset import validate_rows
from src.validation import parse_and_validate,evidence_present
from src.metrics import score
from src import HARMS
def pred(label=0): return {h:{"label":label,"evidence":None if not label else "evidence"} for h in HARMS}
def test_dataset_validation():
    rows=[{"statement_id":"1","statement":"x",**{h:"0" for h in HARMS}}]
    assert validate_rows(rows,True)
    with pytest.raises(ValueError): validate_rows(rows+[rows[0]],True)
    bad=dict(rows[0]); bad["economic"]="2"
    with pytest.raises(ValueError): validate_rows([bad],True)
def test_prediction_validation_and_malformed():
    ok,valid,errors=parse_and_validate(json.dumps(pred())); assert valid and ok
    _,valid,_=parse_and_validate("not json"); assert not valid
    bad=pred(); bad["physical"]={"label":2,"evidence":None}; _,valid,_=parse_and_validate(json.dumps(bad)); assert not valid
def test_evidence(): assert evidence_present("Risk here", "A risk here") is True; assert evidence_present("missing","source") is False
def test_multilabel_metrics():
    truth={"statement_id":"1",**{h:"0" for h in HARMS}}; truth["physical"]="1"
    assert score([{"truth":truth,"parsed_prediction":pred(0)}])["per_harm"][0]["FN"]==1
