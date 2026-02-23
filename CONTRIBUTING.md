# CONTRIBUTING

## Contributing

Contributions are welcome.

- **Bug fixes / typos / docs** — open a PR directly.
- **New features or behaviour changes** — open an issue first to align before
  you invest time.

Keep PRs small and focused. Include a short description of what changed and why,
and confirm that `uv run pytest` passes.

## Project structure

```
git-files-to-prompt/
  src/git_files_to_prompt/  # library code
  tests/
  pyproject.toml
```

## Setup

```sh
uv sync  # installs project + dev dependencies into .venv — nothing touches your host

# verify
uv run python -c "from git_files_to_prompt import files_to_prompt; print('ok')"
uv run git-files-to-prompt --help
```

No runtime dependencies — stdlib only. Dev dependencies (pytest) stay in `.venv/`.

## Installing from this repo

See [README](README.md).

## Tests

```sh
uv run pytest
```

## CI/CD

Two workflows in `.github/workflows/`:

- **`test.yml`** — runs on every push/PR; tests against Python 3.12 and 3.13
- **`publish.yml`** — runs on GitHub Release created; tests, builds, and publishes to PyPI

Publishing uses PyPI trusted publishing (OIDC) — no API token stored in GitHub secrets.

### One-time setup

**PyPI** — go to your PyPI project → *Manage* → *Publishing* → add a trusted publisher:

| Field | Value |
|---|---|
| Owner | your GitHub username |
| Repository | repo name |
| Workflow | `publish.yml` |
| Environment | `release` |

**GitHub** — go to repo *Settings* → *Environments* → create an environment named `release`.

### Release flow

```sh
# 1. bump version in pyproject.toml
#    edit: version = "0.2.0"

# 2. commit and push
git add pyproject.toml
git commit -m "bump version to 0.2.0"
git push

# 3. create a GitHub Release (tag e.g. v0.2.0)
#    GitHub → Releases → Draft a new release
#    CI will run tests → build → publish to PyPI automatically
```

## Publish to PyPI (manual)

```sh
uv build    # creates dist/*.tar.gz and dist/*.whl
uv publish  # prompts for PyPI token

# without the prompt:
# export UV_PUBLISH_TOKEN=pypi-<your-token>
# uv publish
```
