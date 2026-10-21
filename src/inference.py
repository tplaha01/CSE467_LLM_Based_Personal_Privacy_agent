import csv, hashlib, json, platform, time, uuid
from pathlib import Path
from .dataset import load_statements
from .prompt_builder import build_prompt
from .validation import parse_and_validate, evidence_present

def run(adapter, dataset_path, out_dir, config, prompt_path="prompts/harm_detection_v1.txt", limit=None, dry_run=False, resume=False, run_id=None):
    rows=load_statements(dataset_path)[:limit] if limit else load_statements(dataset_path)
    prompt=Path(prompt_path).read_text(encoding="utf-8"); run_id=run_id or uuid.uuid4().hex
    out=Path(out_dir)/run_id; out.mkdir(parents=True, exist_ok=resume); log=out/"run.jsonl"
    manifest={"run_id":run_id,"experiment_config":config,"provider":getattr(adapter,"provider","dry_run"),"model_id":getattr(adapter,"model_id","dry_run"),"prompt_hash":hashlib.sha256(prompt.encode()).hexdigest(),"dataset_hash":hashlib.sha256(Path(dataset_path).read_bytes()).hexdigest(),"python":platform.python_version(),"start_time":time.time()}
    done=set()
    if resume and log.exists(): done={json.loads(x)["statement_id"] for x in log.read_text().splitlines() if x.strip() and json.loads(x).get("validation_status")=="valid"}
    with log.open("a",encoding="utf-8") as f:
        for row in rows:
            if row["statement_id"] in done: continue
            user=build_prompt(row["statement"],prompt_path); record={"experiment_id":config.get("experiment_name"),"run_id":run_id,"statement_id":row["statement_id"],"provider":getattr(adapter,"provider","dry_run"),"model_id":getattr(adapter,"model_id","dry_run"),"prompt_version":config.get("prompt_version"),"prompt_hash":manifest["prompt_hash"],"requested_inference_parameters":config,"timestamp":time.time()}
            if dry_run: record.update(raw_model_response=None,parsed_prediction=None,validation_status="dry_run",parse_success=None,request_metadata={"prompt_length":len(user)}); f.write(json.dumps(record)+"\n"); continue
            try:
                response=adapter.generate("",user,config); parsed,ok,errors=parse_and_validate(response.raw_text)
                record.update(raw_model_response=response.raw_text,parsed_prediction=parsed,validation_status="valid" if ok else "invalid",parse_success=ok,validation_errors=errors,latency_ms=response.latency_ms,input_tokens=response.input_tokens,output_tokens=response.output_tokens,finish_reason=response.finish_reason,request_metadata=response.request_metadata)
            except Exception as e: record.update(raw_model_response=None,parsed_prediction=None,validation_status="error",parse_success=False,error=str(e))
            f.write(json.dumps(record)+"\n")
    manifest.update(end_time=time.time(), samples=len(rows)); (out/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    return run_id
