# Architecture

Open R1 is organized as a small Python package surrounded by recipes and
operational scripts. Training entrypoints share configuration and utilities,
while execution providers isolate untrusted generated code from training jobs.

## Project structure

```text
src/open_r1/
  configs.py                 typed script and training configuration
  sft.py                     supervised fine-tuning entrypoint
  grpo.py                    reinforcement-learning entrypoint
  generate.py                distributed synthetic-data generation
  rewards.py                 reward registry and implementations
  utils/                     datasets, Hub, callbacks, and model helpers
    competitive_programming/ code patching, execution, and scoring
recipes/                     reusable YAML experiment configurations
scripts/                     evaluation, routing, filtering, and data tools
slurm/                       cluster jobs and Piston worker launchers
tests/                       unit tests and credential-dependent slow tests
```

## Training flow

1. `ScriptArguments` validates a single dataset or a weighted mixture.
2. `get_dataset` loads, selects, samples, concatenates, and shuffles examples.
3. `get_model` and `get_tokenizer` resolve model-specific settings.
4. The SFT or GRPO entrypoint creates its TRL trainer and callbacks.
5. Checkpoints and optional Hub revisions are produced by the trainer.

GRPO resolves configured reward names through `get_reward_funcs`. Pure rewards
score text locally. Code rewards delegate execution to an isolated provider and
then normalize the provider result into a numeric reward.

## Execution boundary

Generated code must not execute in the training process. The provider layer
selects E2B, Morph, or Piston and applies timeouts around remote calls. Piston
endpoints are load-balanced with per-endpoint concurrency tokens. Distributed
ranks receive disjoint endpoint subsets to avoid overloading one worker.

The FastAPI routers accept batches of scripts and matching language names. They
validate cardinality and timeouts before acquiring a semaphore and creating a
sandbox. Provider credentials remain server-side and are never part of a batch
payload.

## Evaluation and generation

Generation uses Distilabel to distribute inference and publish generated data.
Evaluation builds LightEval commands from benchmark metadata, determines an
appropriate tensor-parallel size, and can run locally or submit Slurm jobs.
Hub utilities centralize revision naming and metadata uploads.

## Extension points

- Add a reward in `rewards.py` and expose it through the reward registry.
- Add an execution backend behind the provider interface.
- Add a recipe without changing entrypoint code when existing options suffice.
- Add a benchmark definition to the evaluation registry and document hardware.

Keep network access and sandbox lifecycle code out of pure scoring functions.
This separation makes scoring deterministic, supports unit testing, and keeps
credentials and infrastructure failures at a clear system boundary.
