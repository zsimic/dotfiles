# Work overlay

How to apply this personal base before a private work repo on the same machine. Read
[Reuse this setup](./index.md) first for the ownership model and extension points.

## Layout

The work repo takes chezmoi's default location; the personal invocation gets its own root, so the two
never share config, cache, or state:

```text
~/.local/share/chezmoi/      # work source, default chezmoi state; holds both wrappers
~/.local/share/pd/
├── personal-dotfiles/       # personal source
├── chezmoi.toml
├── cache/
└── state.boltdb
```

`~/.local/share/pd` is a local convention; change it consistently in the wrappers if needed.

## Wrappers

Two example scripts to adapt into the root of the work repo (keep them executable):

- [`chezmoi-personal.sh`](./chezmoi-personal.sh) runs chezmoi against the personal root above.
- [`cz.sh`](./cz.sh) is the combined surface: `apply`, `diff`, `status`, …
  run personal first, then work. Other commands are refused unless `WORK_ONLY=1`, which passes them to
  the work invocation alone.

Both call this repo's [check-repo-status] (fetch, and with `PULL=1` rebase a clean repo that is
behind): take it along, or swap in plain `git -C … fetch/pull`.

The personal base already aliases `cz` to `~/.local/share/chezmoi/cz.sh`. Add the scoped aliases to
the work-owned `~/.local/aliases.sh`:

```zsh
alias czp="$HOME/.local/share/chezmoi/chezmoi-personal.sh"
alias czw='WORK_ONLY=1 "$HOME/.local/share/chezmoi/cz.sh"'
```

[check-repo-status]: ../../home/bin/gremlins/executable_check-repo-status

## First setup

Clone the work source without applying it, apply the personal base, then review and apply the work
overlay. This order installs `check-repo-status` before the combined wrapper needs it:

```zsh
chezmoi init git@github.com:your-company/work-dotfiles.git
~/.local/share/chezmoi/chezmoi-personal.sh init --apply https://github.com/you/dotfiles.git
chezmoi diff && chezmoi apply
exec zsh -l
```

A work configuration template still prompts during `chezmoi init`, without touching `$HOME` until the
final apply. Afterwards `cz diff` shows the personal diff first, then the work one.
