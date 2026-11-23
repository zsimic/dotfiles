# Machine setup

This machine is set up by chezmoi-managed dotfiles (see `~/.local/share/chezmoi/AGENTS.md`). To change
a file they manage, this instructions file included, edit its source in the dotfiles repo, not the
copy in `$HOME`.

- CLI tools installed, prefer them when they fit: `rg` (stops at 100 matches per file, add
  `--max-count=0` for all), `fd`, `bat`, `eza`, `tre`, `tokei`, `xh`, `delta`, `duf`, `dua`, `uv`.
  If a missing open-source tool would have helped, say so and offer to add it to the dotfiles.
- In any repo, by default leave edits local and uncommitted (no commits, pushes or PRs), and leave
  applying or deploying them to the user (remind them instead): they follow along with `git diff`.
  Commit or open PRs only when the user or the task (e.g. a ticket) asks for it.
- Scratch files go in `_tmp/` at the repo root (git-ignored everywhere), never `/tmp`.
- github.com remotes stay on https, pushes go over ssh via `pushInsteadOf`: see `{here}/github.md`.

# Working together

- Disagree out loud: when a request rests on a wrong assumption, misses a case, or has a better
  alternative, say so before acting on it, with the tradeoff.
- Writing code in a repo that holds domain state and will grow: model concepts as classes that own
  their data and behavior; read `{here}/code-design.md` for the signs of a missing class.
- Creating or refreshing repo docs: read the “Code is the authority” guidance in
  `{here}/repo-docs.md` first.
