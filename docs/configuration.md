# Configuration reference

Open R1 accepts command-line arguments directly or reads the same values from
YAML recipe files. Command-line values override recipe values, making it easy
to reuse a checked-in recipe while changing a model or output path for one run.

## Dataset selection

Set `dataset_name` for one Hub dataset and optionally set `dataset_config`.
Alternatively, configure `dataset_mixture.datasets` with one or more entries.
Each mixture entry supports an `id`, `config`, `split`, `columns`, and a weight
greater than zero and no greater than one. The two modes are mutually exclusive.

```yaml
dataset_mixture:
  seed: 42
  test_split_size: 0.1
  datasets:
    - id: open-r1/Mixture-of-Thoughts
      split: train
      columns: [messages]
      weight: 0.5
```

## Environment variables

| Variable | Required when | Purpose |
| --- | --- | --- |
| `HF_TOKEN` | Private Hub resources | Authenticates downloads and uploads. |
| `WANDB_API_KEY` | W&B reporting | Authenticates experiment logging. |
| `WANDB_ENTITY` | Optional | Overrides the W&B account or team. |
| `WANDB_PROJECT` | Optional | Selects the W&B project. |
| `MORPH_API_KEY` | Morph execution | Authenticates Morph sandboxes. |
| `E2B_API_KEY` | E2B execution | Authenticates E2B sandboxes. |
| `PISTON_ENDPOINTS` | Piston rewards | Comma-separated HTTP(S) worker URLs or `slurm`. |
| `PISTON_MAX_REQUESTS_PER_ENDPOINT` | Optional | Positive concurrency limit per worker. |
| `LOCAL_RANK` / `WORLD_SIZE` | Distributed execution | Partitions Piston workers among ranks. |
| `CF_TESTS_FOLDER` | Codeforces scoring | Location of extracted Codeforces tests. |

Keep secrets in the process environment or an ignored `.env` file. Never add
tokens to YAML recipes, Slurm files, shell history, or Git commits.

## Validating a recipe

Use a small model and a short dataset slice before starting an expensive run.
Confirm that selected columns exist, mixture weights are valid, the output path
has enough storage, and remote execution endpoints respond to health checks.

## Hosted execution

E2B and Morph require credentials and outbound network access. Piston can be
self-hosted; each endpoint must include an `http://` or `https://` scheme.
Batch requests require non-empty script and language arrays of equal length,
plus positive execution and request timeouts.
