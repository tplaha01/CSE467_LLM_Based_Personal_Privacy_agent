import argparse,yaml
from pathlib import Path
from adapters import create_adapter
from .inference import run
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--model",required=True); ap.add_argument("--limit",type=int); ap.add_argument("--dry-run",action="store_true"); ap.add_argument("--resume",action="store_true"); ap.add_argument("--run-id"); ap.add_argument("--config",default="config/experiment.yaml"); ap.add_argument("--models",default="config/models.yaml"); a=ap.parse_args()
    cfg=yaml.safe_load(Path(a.config).read_text()); models=yaml.safe_load(Path(a.models).read_text())["models"]
    if a.model not in models: raise SystemExit(f"unknown model alias: {a.model}")
    m=models[a.model]; adapter=create_adapter(m["provider"],m["model"])
    if not a.dry_run and m["model"].startswith("REPLACE_"): raise SystemExit("configure an exact model ID before live inference")
    if a.resume and not a.run_id: raise SystemExit("--resume requires --run-id for an existing run")
    rid=run(adapter,cfg["dataset_path"],cfg["prediction_dir"],cfg,limit=a.limit,dry_run=a.dry_run,resume=a.resume,run_id=a.run_id); print(rid)
if __name__=="__main__": main()
