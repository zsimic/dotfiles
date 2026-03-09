# Repository Guidelines

## Purpose
- This repository manages personal dotfiles with `chezmoi`.
- The setup is intentionally minimal, for example `oh-my-zsh` avoided here (too bloated)
- Ideally `bash` and `zsh` setup stays similar wherever applicable.
  - `zsh` is preferred and used in most cases, but some machines targetted by this are still on `bash`
  - Keep all key settings like PATH identical between `bash` and `zsh`
- Keep the repo safe to publish: do not add secrets, tokens, private keys, machine-specific credentials, or exported secure defaults databases.

## Layout
- `home/` mirrors the target home directory as expected by `chezmoi`.
- Keep platform-specific files grouped in platform-specific directories when possible.
- Prefer whole-file platform splits plus `home/.chezmoiignore` when that keeps the layout simpler, but do not force extra file splits when a single `.tmpl` is clearer.
- `home/.chezmoiscripts/` contains lifecycle scripts. Darwin-only scripts belong under `home/.chezmoiscripts/darwin/`.
- `tests/` contains automated tests for Python helpers and similar logic.
- `resources/` is for checked-in supporting material, not generated output.

## Implementation Preferences
- Prefer plain tracked files over `chezmoi` `.tmpl` files when static files work, but use a `.tmpl` when it makes the overall design simpler or more extensible.
- A single clear template is preferable to multiple plain files plus glue when the template stays readable.
- If templating is necessary, keep the rendered outcome and the template structure obvious.
- Python is used for non-trivial logic, parsing, or anything that benefits from tests.
- Favor simple, standard-library-heavy solutions over extra dependencies.
- Preserve existing naming conventions used by `chezmoi`, such as `dot_*`, `executable_*`, and `run_*`.

## Shell Conventions
- Use best-practice shell conventions
- Do not use XDG env vars
  - Use `"$HOME/.config"` instead of `$XDG_CONFIG_HOME` etc.
  - We are just defining them for good measure for a handful of tools that operate better with them defined
  - This repo's file layout under `home/` will not accommodate any XDG esoteric setup anyway
- Keep shell scripts idempotent and safe to re-run.
- The setup aims to be more and more best-practice (not quite there yet)

## Testing
- When python files are modified:
  - Run `tox` when python files were modified.
  - Run `tox -e style` for linting and formatting checks.
  - New Python logic should include tests in `tests/` when practical.
  - Aim for full coverage when reasonable. If a change makes full coverage impractical, call out the gap explicitly.
  - Keep test fixtures small and readable.

## Chezmoi Conventions
- Prefer directory layout over template conditionals for OS-specific content when it materially simplifies the repo, but a single template is fine when that is the cleaner shape.
- If something is macOS-only, keep it under a macOS-specific path that can be ignored as a group.
- Avoid embedding secrets in templates or data values.
- Default to `run_onchange_` script variants for `chezmoi` hooks.
- Assume `chezmoi` scripts should be idempotent and safe to re-run.
- Use `run_onchange_` scripts for side effects that should happen when managed content changes.
- Reach for other `run_*` variants only when `run_onchange_` is clearly not the right fit.
- Keep `run_*` script side effects narrow, predictable, and tied to specific managed files.
- If an external app needs a restart after config changes, prefer a dedicated `run_onchange_after_*` script scoped to that app.
- Use `.chezmoiremove` to clean up files that should disappear from target machines after layout changes.
- Keep files under `home/` only when they are meant to be materialized into `$HOME` on the target machine.
- Keep repo-only source assets outside `home/` when they do not need to exist separately on the target system.
- Prefer files that remain pleasant to edit in normal IDEs; `.tmpl` files are fine when they stay readable and simplify the surrounding structure.

## Change Discipline
- Make the smallest coherent change that improves the repo.
- Preserve the current style unless there is a clear reliability or maintainability win.
- When introducing a new convention, apply it consistently in the affected area.
- If you add a new tool, script, or layout pattern, update documentation or tests in the same change when needed.
- Never commit, merge, or rewrite Git history. Leave changes uncommitted for inspection with `git diff`.
