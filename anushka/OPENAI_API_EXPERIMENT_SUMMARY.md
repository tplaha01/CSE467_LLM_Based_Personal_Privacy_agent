# OpenAI API Experiment - Anushka

## Experiment

- Provider: OpenAI API
- Model: `gpt-4o-mini`
- Statements: 50
- Run ID: `823ec0f48cf947d384a6e5644cd79ecf`
- Valid outputs: 50/50 (100%)
- Average latency: approximately 2.66 seconds per request

## Overall metrics

- Micro precision: 0.4667
- Micro recall: 0.1795
- Micro F1: 0.2593
- Macro precision: 0.2088
- Macro recall: 0.0714
- Macro F1: 0.1035
- Exact-match accuracy: 0.44
- Hamming loss: 0.1143

## Per-harm results

| Harm | TP | FP | TN | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| physical | 0 | 1 | 47 | 2 | 0.0000 | 0.0000 | 0.0000 |
| economic | 1 | 0 | 46 | 3 | 1.0000 | 0.2500 | 0.4000 |
| reputational | 0 | 0 | 47 | 3 | 0.0000 | 0.0000 | 0.0000 |
| psychological | 0 | 0 | 44 | 6 | 0.0000 | 0.0000 | 0.0000 |
| autonomy | 6 | 7 | 19 | 18 | 0.4615 | 0.2500 | 0.3243 |
| discrimination | 0 | 0 | 50 | 0 | 0.0000 | 0.0000 | 0.0000 |
| relationship | 0 | 0 | 50 | 0 | 0.0000 | 0.0000 | 0.0000 |

## Artifacts

- `predictions/823ec0f48cf947d384a6e5644cd79ecf/` contains the raw responses and manifest.
- `results/823ec0f48cf947d384a6e5644cd79ecf/` contains metrics, errors, and predictions joined with ground truth.

The first network-blocked attempt is retained separately under prediction run `9647d6de3e1e47158491574c79d97808`; it contains 50 connection errors and was not used for the reported metrics.
