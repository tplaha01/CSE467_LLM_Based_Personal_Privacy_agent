# Open-Source LLM Experiments - Tarandeep

Date: 2026-10-21

## Research task

This work evaluates whether a locally run open-source LLM can identify seven privacy harms in privacy-policy statements:

`physical`, `economic`, `reputational`, `psychological`, `autonomy`, `discrimination`, and `relationship`.

The experiment uses the group's shared 50-statement dataset, harm taxonomy, prompt, JSON schema, validation code, and evaluation metrics. Ground-truth labels are used only during evaluation.

## Models and runs

### Llama 3.2 3B

- Model: `llama3.2:3b`
- Run ID: `b851687f433b49d48470733d7b2f6161`
- Statements: 50
- Valid outputs: 6/50 (12%)
- Invalid outputs: 44/50 (88%)
- Macro F1: 0.00
- Micro F1: 0.00
- Exact-match accuracy: 0.52
- Average latency: approximately 2.13 seconds per request

The main failure was returning the string `"null"` instead of JSON `null`, which violated the shared schema.

### Qwen 4B

- Model: `qwen:4b` Q4_0 GGUF
- Run ID: `a66d49fda5ea4b5797c1b55477bcfa76`
- Statements: 50
- Valid outputs: 50/50 (100%)
- Invalid outputs: 0/50 (0%)
- Macro F1: 0.00
- Micro F1: 0.00
- Exact-match accuracy: 0.52
- Average latency: approximately 11.07 seconds per request

The native Ollama structured-output schema fixed the formatting problem. However, Qwen 4B predicted every harm label as 0. It therefore missed all positive harm labels, including 24 positive autonomy labels.

The 0.52 exact-match score is not evidence of useful performance. The dataset is imbalanced, and an all-negative classifier also obtains 0.52 exact-match accuracy.

## Current conclusion

At this stage, local open-source inference is technically reproducible, but the tested models do not provide reliable privacy-harm identification:

1. Llama 3.2 3B had poor schema compliance and produced mostly invalid outputs.
2. Qwen 4B achieved complete schema compliance after native structured-output support was added.
3. Qwen 4B still failed the substantive task by collapsing to all-negative predictions.
4. The meaningful performance measures are therefore macro-F1, micro-F1, recall, per-harm recall, and output-validity rate—not exact-match accuracy alone.

These results should be reported as an open-source baseline, not as evidence that open-source LLMs generally cannot perform the task. The evidence is limited to the tested model sizes, quantizations, prompt, taxonomy, and local inference configuration.

## Deviation from the original project plan

The original plan assumed that the open-source LLM experiment could be run and compared directly with the other model families. The results created a necessary deviation from that plan: before treating the open-source result as a fair research conclusion, the experiment must be verified with additional instruction-tuned open-source models and, if needed, stronger model sizes.

The next validation should compare multiple models while holding the dataset, prompt, taxonomy, temperature, output schema, and evaluator constant. Candidate models should be selected based on both task quality and available VRAM. If suitable models cannot run reliably on the local RTX 3050 Ti 4 GB GPU, the group should run the same harness on the ASU Sol computing server, record the exact model/quantization/runtime configuration, and preserve all raw outputs and manifests.

This deviation is important for research validity: the current Qwen result demonstrates a model-specific failure mode, not a general conclusion about open-source LLMs.

## Framework fixes made during the experiment

- Restored the missing `prompts/harm_detection_v1.txt` artifact from the checked-in taxonomy and schema.
- Fixed OpenAI-compatible `max_output_tokens` handling.
- Corrected micro-precision and micro-recall calculation.
- Hardened evaluation against malformed prediction objects.
- Added native Ollama structured-output support using `schemas/prediction.schema.json`.
- Kept raw model responses and invalid outputs in the prediction artifacts.

All repository tests pass: `4 passed`.

## Artifact locations

- `predictions/` contains every smoke, failed, and full run.
- `results/` contains the evaluated metrics and error analyses.
- The primary comparison runs are `b851687f433b49d48470733d7b2f6161` (Llama 3.2 3B) and `a66d49fda5ea4b5797c1b55477bcfa76` (Qwen 4B).
