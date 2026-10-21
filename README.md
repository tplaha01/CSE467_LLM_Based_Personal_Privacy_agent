# Privacy Harm Evaluation Framework

This project measures how well different LLMs identify seven privacy harms in privacy-policy statements: `physical`, `economic`, `reputational`, `psychological`, `autonomy`, `discrimination`, and `relationship`.

Every teammate uses the same dataset, taxonomy, prompt, output schema, validation rules, and evaluation code. Only the provider and model ID change. Ground-truth labels are used only during evaluation and are never sent to a model.

## Running Your Assigned Model

### 1. Install Python

Use Python 3.11 or newer.

Windows: install Python from [python.org](https://www.python.org/downloads/windows/) and enable **Add Python to PATH**.

macOS: install Python from [python.org](https://www.python.org/downloads/macos/) or run `brew install python`.

Check it:

```bash
python --version
```

If macOS does not recognize `python`, use `python3` in every command below.

### 2. Clone the repository

```bash
git clone https://github.com/tplaha01/CSE467_LLM_Based_Personal_Privacy_agent.git
cd CSE467_LLM_Based_Personal_Privacy_agent
```

### 3. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If activation is blocked, run this once as your normal user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Add your API key

Windows:

```powershell
Copy-Item .env.example .env
notepad .env
```

macOS/Linux:

```bash
cp .env.example .env
nano .env
```

Add only the key for your assigned provider. Never commit or share `.env`.

### 6. Configure your assigned model

Edit `config/models.yaml` and add or edit one model entry:

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

Use the exact model ID supplied by the provider. Do not change Python code, the prompt, or evaluation logic.

| Provider | `provider` value | `.env` variable |
|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` |
| Google Gemini | `google` | `GOOGLE_API_KEY` |
| OpenAI-compatible gateway | `openai_compatible` | `TOKENROUTER_API_KEY` and `OPENAI_COMPATIBLE_BASE_URL` |
| Local Hugging Face | `local_hf` | no API key |

### 7. Run an offline dry run

This constructs prompts without contacting a provider or spending money:

```bash
python -m src.run_experiment --model my_openai --limit 3 --dry-run
```

The command prints a `RUN_ID`. Save it for evaluation.

### 8. Run the experiment

Small test run:

```bash
python -m src.run_experiment --model my_openai --limit 3
```

Full run:

```bash
python -m src.run_experiment --model my_openai
```

Replace `my_openai` with your configured model alias. Each run uses independent single-turn requests and stores raw responses. Ground-truth labels are not sent to providers.

### 9. Resume an interrupted run

```bash
python -m src.run_experiment --model my_openai --run-id RUN_ID --resume
```

Successfully completed statements are skipped. Invalid and failed outputs remain visible.

### 10. Evaluate the run

```bash
python -m src.evaluate --run RUN_ID
```

Results are written to `results/RUN_ID/`:

- `metrics.json`
- `overall_metrics.csv`
- `per_harm_metrics.csv`
- `predictions_with_ground_truth.csv`
- `errors.csv`

Metrics include micro/macro precision, recall, and F1; exact-match accuracy; Hamming loss; and TP, FP, TN, FN, and support for every harm.

## Testing

After installing requirements:

```bash
python -m pytest -q
```

Tests are offline and do not require API keys or paid API calls.

## Output and reproducibility

Each run is stored under `predictions/RUN_ID/` with raw responses, parsed predictions, validation status, provider and exact model ID, inference parameters, latency, token counts when available, prompt/taxonomy/dataset hashes, and a manifest.

Do not manually correct predictions. Failed and malformed responses must remain in the run output.

## Data files

- `data/ground_truth.csv`: statement text and reconciled human labels.
- `data/statements.csv`: inference-only file containing only `statement_id` and `statement`.
- `prompts/harm_detection_v1.txt`: canonical prompt.
- `config/taxonomy.json`: shared harm definitions.
- `schemas/prediction.schema.json`: required output schema.

The current dataset was converted from the teammate annotation workbook. Do not replace it with a personal subset or modify labels manually.

## Security rules

- Never commit `.env` or API keys.
- Never send `ground_truth.csv` to a provider.
- Never create provider-specific prompt variants.
- Never overwrite an existing prediction run.
- Share only artifacts approved by the research team.
