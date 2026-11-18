# Machine setup

This machine is set up by chezmoi-managed dotfiles (see `~/.local/share/chezmoi/AGENTS.md`). To change
a file they manage, this instructions file included, edit its source in the dotfiles repo, not the
copy in `$HOME`.

- CLI tools installed, prefer them when they fit: `rg` (stops at 100 matches per file, add
  `--max-count=0` for all), `fd`, `bat`, `eza`, `tre`, `tokei`, `xh`, `delta`, `duf`, `dua`, `uv`.
  If a missing open-source tool would have helped, say so and offer to add it to the dotfiles.
- Scratch files go in `_tmp/` at the repo root (git-ignored everywhere), never `/tmp`.
- github.com remotes stay on https, pushes go over ssh via `pushInsteadOf`: see `{dotfiles}/agents/github.md`.
- Creating or refreshing repo docs: read `{dotfiles}/agents/repo-docs.md` first.
