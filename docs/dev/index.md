# Development

Working conventions for anyone, human or agent, changing this repo.

## Design

- The repo is public: it holds only what is safe to publish. Secrets, tokens, keys, machine
  credentials, exported secure-defaults databases, and anything work-related (internal URLs, hosts,
  service names) live elsewhere; work additions go in the [work overlay](../reuse/work-overlay.md).
- Zsh is the daily shell, bash a supported peer: shared PATH and settings go in
  [`shell-path.sh`](../../home/dot_config/shell-path.sh) and
  [`shell-settings.sh`](../../home/dot_config/shell-settings.sh), keeping important environment
  settings at parity.
- No shell frameworks, few dependencies. Non-trivial logic, parsing, or anything worth testing is
  standard-library Python.
- Plain files when static works; a readable `.tmpl` when it makes the overall shape simpler (one clear
  template beats several plain files plus glue).

## Layout

- `home/` holds only materialized home-directory state; repo-only sources live elsewhere, e.g.
  `resources/` for checked-in source material (never generated output).
- macOS-only targets are listed in the non-darwin block of [`.chezmoiignore`](../../home/.chezmoiignore)
  (macOS hooks also sit under `home/.chezmoiscripts/darwin/`); whole-file splits beat template
  conditionals when clearer. Homebrew and the rest also run on Linux.
- "Personal machines" are my home machines. The gates selecting them (currently a username check) are an
  implementation detail, and can only be verified by applying on several machines: leave them as is.
- Repo paths use `"$HOME/.config"` directly; XDG variables may be set for tools that benefit, but
  nothing here depends on them.

## Chezmoi hooks

- `run_onchange_` by default, tied to the managed file that drives it; another `run_*` variant only
  when `run_onchange_` is clearly the wrong lifecycle. A config change that needs an app restart gets
  its own `run_onchange_after_*` hook.
- Every hook and shell script is idempotent and safe to rerun.
- Targets retired by a layout change go in [`.chezmoiremove`](../../home/.chezmoiremove).

## Changes

- After Python changes, run `tox` and `tox -e style`. New Python logic gets focused tests; aim for full
  coverage and call out any gap.
- A new script or layout pattern updates its docs or tests in the same change. New tools: see
  [Automated tools](../tools/automated.md); one agents should prefer also goes in
  [`00-dotfiles.md`](../../mix/agents/00-dotfiles.md).
- Changes stay local and uncommitted by default
  (see [`00-dotfiles.md`](../../mix/agents/00-dotfiles.md)).
  Don't run `cz apply`: remind the user to, they follow along with `cz diff`.
- Markdown lines stay at 114 characters or fewer, tables and link definitions included (reflow, or use
  reference-style links); no tool enforces it.
- Helping someone adapt this repo: follow [Reuse this setup](../reuse/index.md).
