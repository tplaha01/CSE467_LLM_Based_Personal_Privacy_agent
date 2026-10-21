# Privacy Harm Evaluation Framework

This repository evaluates LLM multi-label classification of seven privacy harms using one versioned taxonomy, prompt, output schema, validation path, and metrics implementation for every provider. Inference and ground truth are intentionally separated: inference loads only `statement_id` and `statement`; evaluation loads labels afterward.

## Architecture

```
Ground Truth CSV -> Statement Loader -> Canonical Prompt -> Provider Adapter
                                                   |              |
                                                   +---- GPT / Claude / Gemini / open source
                                                                  v
                                                        Schema Validator -> JSONL Predictions
                                                                  v
                                                   Evaluation -> Metrics + Error Analysis
```

The categories are physical, economic, reputational, psychological, autonomy, discrimination, and relationship. The canonical annotation rules live in `prompts/harm_detection_v1.txt`; change the version when changing the prompt.

## Running Your Assigned Model

1. `python -m venv .venv` and activate it.
2. `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and add only the required key.
4. Set the exact model ID in `config/models.yaml`.
5. Test without API calls: `python -m src.run_experiment --model open_source --limit 3 --dry-run`.
6. Run: `python -m src.run_experiment --model <assigned_model>`.
7. Evaluate: `python -m src.evaluate --run <RUN_ID>`.

Each run receives a unique ID and writes raw responses, parsed predictions, validation state, parameters, hashes, timing, and a manifest under `predictions/<run_id>/`. Existing runs are never overwritten. `--resume` skips valid completed statements in a run. No model history or ground-truth labels are sent to providers.

## Provider setup

Choose the provider in `config/models.yaml`; no Python changes are needed:

```yaml
models:
  my_openai:
    provider: openai
    model: gpt-4o-mini
  my_anthropic:
    provider: anthropic
    model: claude-3-5-sonnet-latest
  my_google:
    provider: google
    model: gemini-1.5-flash
  my_gateway:
    provider: openai_compatible
    model: provider/model-id
  my_local:
    provider: local_hf
    model: organization/model-id
```

Set only the matching key in `.env`: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, or `TOKENROUTER_API_KEY` plus `OPENAI_COMPATIBLE_BASE_URL` for a compatible gateway. Then run `python -m src.run_experiment --model my_openai`. All providers receive the same statement, taxonomy, prompt, output schema, and evaluation logic; only the adapter and model endpoint differ. Direct providers use their official SDKs, while compatible gateways use the OpenAI chat-completions protocol. Local Hugging Face runs require suitable hardware and the `torch`/`transformers` dependencies.

## Testing and reproducibility

Run `pytest -q`. The included three-row dataset and tests are offline and consume no API credits. Evaluation reports micro/macro precision, recall, F1, exact-match accuracy, Hamming loss, and TP/FP/TN/FN plus per-harm metrics. Prompt, taxonomy, and dataset hashes are recorded in manifests. Do not commit `.env`, API keys, or unreviewed artifacts.

## Data format

`data/ground_truth.csv` contains statement text plus exactly 0/1 labels. It is validated for missing/duplicate IDs, duplicate statements, missing text/columns, and invalid labels. `data/statements.csv` is the inference-only form. Replace the synthetic files with the reconciled research dataset before the real run.
