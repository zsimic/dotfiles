# Development and adaptation

This section is the working contract for humans and LLMs changing the repository. The setup is
intentionally minimal, public-safe, and centered on obvious files plus narrow chezmoi lifecycle
hooks.

## Design

- This repository manages personal dotfiles with [chezmoi](https://www.chezmoi.io/) and must remain
  safe to publish.
- Zsh is preferred, but bash remains supported. Keep PATH and shared behavior aligned through
  [`shell-path.sh`](../../home/dot_config/shell-path.sh) and
  [`shell-settings.sh`](../../home/dot_config/shell-settings.sh).
- Avoid shell frameworks and dependencies that do not earn their maintenance cost.
- Never add secrets, tokens, private keys, machine-specific credentials, or exported secure-defaults databases.
- Prefer plain tracked files when static files work. Use a readable `.tmpl` when it makes the
  overall shape simpler.
- Prefer one clear template to multiple plain files plus glue when the template remains readable.
- Keep template structure and rendered output obvious. Files should remain pleasant to edit in a
  normal IDE.
- Use Python for non-trivial logic, parsing, or work that benefits from tests.
- Favor simple, standard-library-heavy solutions over extra dependencies.

## Repository layout

- [`home/`](../../home/) mirrors the target home directory as chezmoi source state.
- Group platform-specific files under platform-specific directories when practical.
- [`home/.chezmoiscripts/`](../../home/.chezmoiscripts/) contains lifecycle hooks; macOS hooks stay
  under `darwin/`.
- [`resources/`](../../resources/) contains checked-in source material that is not independently
  materialized in `$HOME`; it is not for generated output.
- [`tests/`](../../tests/) contains automated tests for Python helpers and similar logic.
- Preserve chezmoi naming such as `dot_*`, `executable_*`, and `run_*`.

## Chezmoi conventions

- Default to `run_onchange_` for side effects that should run when their managed input changes.
- Use another `run_*` variant only when `run_onchange_` is clearly the wrong lifecycle.
- Keep hook side effects narrow, predictable, and tied to specific managed files. Every hook must be
  idempotent and safe to rerun.
- Prefer a dedicated `run_onchange_after_*` hook when an application must restart after a configuration change.
- Prefer whole-file platform splits plus [`.chezmoiignore`](../../home/.chezmoiignore) when that is
  clearer than template conditionals. Keep a single template when it is the simpler shape.
- Never embed secrets in templates or chezmoi data values.
- Use [`.chezmoiremove`](../../home/.chezmoiremove) for target files that should disappear after a layout change.
- Keep only materialized home-directory state under `home/`; keep repository-only sources elsewhere.

## Shell conventions

- Follow best-practice shell conventions and improve the setup incrementally rather than through
  unnecessary broad rewrites.
- Use `"$HOME/.config"` directly rather than routing repository paths through XDG variables.
- XDG variables may be defined for tools that benefit from them, but repository paths must not
  depend on an alternate XDG layout.
- Keep shell scripts idempotent and safe to rerun.
- Preserve bash/zsh parity for important environment settings, while using shell-native
  implementation where appropriate.

## Testing

- After Python changes, run `tox` plus `tox -e style` for linting and formatting checks.
- Add focused tests for new Python logic when practical.
- Aim for full coverage when reasonable; call out any coverage gap explicitly.
- Keep test fixtures small and readable.

## Change discipline

- Make the smallest coherent change and preserve the surrounding style unless there is a clear
  maintenance or reliability win.
- Apply a new convention consistently within the affected area.
- When adding a tool, script, or layout pattern, update the relevant documentation or tests in the
  same change.
- Agents never commit, merge, or rewrite Git history. Leave changes uncommitted for inspection with
  `git diff`.
- Keep Markdown source lines at 114 characters or fewer, including tables and link definitions.
  Reflow prose or use reference-style links when needed.

## Reusing the setup

[Reuse this setup](../reuse/index.md) is the external-facing guide for adapting this repository into
a new personal setup. It also documents the two-repository wrapper used to apply a shared personal
base before a private work overlay without weakening the public repository boundary.

An LLM following that guide should ask for repository URLs and ownership decisions, inspect
existing destination files, and ask before applying changes to the live home directory.
