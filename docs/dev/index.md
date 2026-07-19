# Development and adaptation

This section is the working contract for humans and LLMs changing the repository. The setup is intentionally minimal, public-safe, and centered on obvious files plus narrow chezmoi lifecycle hooks.

## Design

- Zsh is preferred, but bash remains supported. Keep PATH and shared behavior aligned through [`shell-path.sh`](../../home/dot_config/shell-path.sh) and [`shell-settings.sh`](../../home/dot_config/shell-settings.sh).
- Avoid shell frameworks and dependencies that do not earn their maintenance cost.
- Never add secrets, tokens, private keys, machine-specific credentials, or exported secure-defaults databases.
- Prefer plain tracked files when static files work. Use a readable `.tmpl` when it makes the overall shape simpler.
- Prefer standard-library Python for non-trivial parsing or logic, with tests when practical.

## Repository layout

- [`home/`](../../home/) mirrors the target home directory as chezmoi source state.
- [`home/.chezmoiscripts/`](../../home/.chezmoiscripts/) contains lifecycle hooks; macOS hooks stay under `darwin/`.
- [`resources/`](../../resources/) contains checked-in source material that is not independently materialized in `$HOME`.
- [`tests/`](../../tests/) contains automated tests for Python helpers and similar logic.
- Preserve chezmoi naming such as `dot_*`, `executable_*`, and `run_*`.

## Chezmoi conventions

- Default to `run_onchange_` for side effects that should run when their managed input changes.
- Keep hooks narrow, predictable, idempotent, and safe to rerun.
- Prefer a dedicated `run_onchange_after_*` hook when an application must restart after a configuration change.
- Prefer platform directories plus [`.chezmoiignore`](../../home/.chezmoiignore) when that is clearer than template conditionals.
- Use [`.chezmoiremove`](../../home/.chezmoiremove) for target files that should disappear after a layout change.
- Keep only materialized home-directory state under `home/`; keep repository-only sources elsewhere.

## Shell conventions

- Use `"$HOME/.config"` directly rather than routing repository paths through XDG variables.
- Keep shell scripts idempotent and safe to rerun.
- Preserve bash/zsh parity for important environment settings, while using shell-native implementation where appropriate.

## Change and test discipline

- Make the smallest coherent change and preserve the surrounding style unless there is a clear maintenance or reliability win.
- Apply a new convention consistently within the affected area and update documentation with the implementation.
- Run `tox` and `tox -e style` after Python changes. Add focused tests and aim for full coverage when practical.
- Agents leave changes uncommitted for inspection and do not merge or rewrite Git history unless explicitly asked.

## Adapting the pattern

The reusable shape from the former getting-started guide is intentionally small:

1. Install [chezmoi](https://www.chezmoi.io/install/) and create a source repo.
2. Track shell and tool configuration under chezmoi's source naming conventions.
3. Add a tiny daily wrapper like [`cz.sh`](../../cz.sh) for remote status plus normal chezmoi commands.
4. Add a rerunnable entry point like [`bootstrap.sh`](../../bootstrap.sh) for prerequisites and `chezmoi init --apply`.

The wrapper keeps normal use terse:

```console
cz
cz fetch
cz apply
cz update
```

For private or work-only configuration, keep a second private chezmoi source as a thin layer rather than weakening the public repository boundary. Apply the public/personal source first and the private source second; a wrapper can expose both as one workflow. [`check-repo-status`](../../home/bin/gremlins/executable_check-repo-status) is the small reusable helper behind the per-repository status display.

When an LLM is adapting this setup for someone else, it should preserve that structure, ask before applying changes to the live home directory, and avoid inventing private values or committing secrets.
