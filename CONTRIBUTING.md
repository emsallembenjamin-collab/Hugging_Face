# Contributing to Open R1

Thank you for improving Open R1. Keep changes focused, explain operational
assumptions, and add tests for behavior that can run without costly hardware.

## Development setup

Install Python 3.11, `uv`, Git LFS, and the CUDA version documented in the
README. The full development environment is GPU-oriented and may take several
minutes to build.

```shell
make install
```

For documentation or isolated utility work, a smaller environment may be
sufficient, but record any checks omitted because optional dependencies were
not installed.

## Quality checks

Run formatting and static checks before opening a pull request:

```shell
make style
make quality
```

Run fast tests without hosted sandbox credentials:

```shell
make test
```

Slow tests call E2B or Morph and require credentials, network access, and
available service capacity:

```shell
make slow_test
```

The package does not have a separate compile step. Building a distributable
artifact can be checked with `python -m build` after installing `build`.

## Change workflow

1. Create a descriptive branch from an up-to-date `main`.
2. Make one coherent change and include regression coverage where practical.
3. Review `git diff --check` and `git diff` before committing.
4. Run the checks relevant to the files you changed.
5. Use a concise Conventional Commit-style subject.
6. Push the branch and describe hardware, credentials, or checks not available.

Do not commit API tokens, generated model weights, local datasets, `.env`
files, or experiment outputs. Prefer environment variables for credentials and
small configuration examples with placeholder values in documentation.

## Testing guidance

- Unit-test parsing and validation without network calls.
- Mock Hub datasets and hosted providers at their module boundary.
- Keep credential-dependent scenarios under `tests/slow/`.
- Test both valid input and the failure message for rejected input.
- Avoid tests that depend on ordering unless ordering is part of the contract.

## Troubleshooting

If imports resolve to an installed release instead of this checkout, confirm
that `PYTHONPATH=src`; the Make targets set it automatically. CUDA or vLLM
binary errors usually indicate a mismatch with the documented PyTorch/CUDA
versions. Authentication failures should be checked independently with the
Hugging Face, W&B, E2B, or Morph client before debugging training code.

For Piston errors, verify every URL includes a scheme, `/api/v2` is reachable,
and the number of workers is sufficient for `WORLD_SIZE`. For dataset mixtures,
check IDs, selected columns, weights, and test split size before allocating GPUs.
