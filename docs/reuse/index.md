# Reuse this setup

This guide is for someone who wants the same shape as this repository: a small, public-safe
personal dotfiles base that works across home machines and can also sit underneath a private work
layer.

> Suggested prompt: “Read `docs/reuse/index.md` from `github.com/zsimic/dotfiles` and help me
> adapt this setup for my own personal and work environments. Ask for the missing repository URLs
> and preferences before changing files or applying anything.”

This repository is a reference, not a universal manifest. Keep the architecture; choose your own
applications and tools from the [documented inventory](../tools/index.md). Do not run its bootstrap
unchanged for another user: it intentionally applies Zoran's source state only for the `zoran`
account.

## What to reuse

- A framework-free bash/zsh base with shared PATH and shell settings.
- A checked-in package inventory plus narrow, idempotent chezmoi lifecycle hooks.
- A rerunnable [`bootstrap.sh`](../../bootstrap.sh) for a fresh personal machine.
- A small [`cz.sh`](../../cz.sh) wrapper for remote status plus normal chezmoi commands.
- Explicit extension points where a private work repo can add configuration without copying or
  replacing the shared base.

Read the [repository overview](../../README.md) for the design and
[development notes](../dev/index.md) for its working conventions.

## Choose the shape

### Personal machines

The personal repo is the normal chezmoi source at `~/.local/share/chezmoi` and applies directly to
`$HOME`. The standard bootstrap and `cz` wrapper are sufficient.

### Work machines

The private work repo becomes the normal chezmoi source at `~/.local/share/chezmoi`. The personal
repo is cloned separately with its own config, cache, and persistent state. The work wrapper
invokes both:

```text
personal source + isolated chezmoi state ── apply first ──┐
                                                          ├── $HOME
work source + default chezmoi state ────── apply second ──┘
```

This is ordered application, not native chezmoi composition or file-level merging. Prefer disjoint
target files. If both repos manage the same target, the work version wins after the combined apply,
but the personal repo may continually report that target as changed.

## Use extension points

The personal base deliberately loads optional files that a work repo can own:

| Work-owned target | Loaded by the personal base | Purpose |
| --- | --- | --- |
| `~/.local/shell-path.sh` | [shell-path] | Work-only PATH and environment setup |
| `~/.local/aliases.sh` | [shell-settings] | Work-only aliases and shell functions |
| `~/.config/git/config-work` | [git-config] | Work identity, hosts, and Git behavior |

[shell-path]: ../../home/dot_config/shell-path.sh
[shell-settings]: ../../home/dot_config/shell-settings.sh
[git-config]: ../../home/dot_config/git/config

Use the same pattern for new integration points: let the personal repo own the stable parent
configuration and optionally load a separate file owned by the work repo.

## Questions the assistant should resolve

Before implementing anything, ask:

1. Is the personal base a fork of this repo or a new repo using it as a reference?
2. What are the personal and work Git URLs, and which are private?
3. Which operating systems and usernames must be supported?
4. Which tools and applications from the inventory should actually be automated?
5. Which work-only files are needed, and can they use the existing extension points?
6. Where will secrets live? They must not be committed to either source state as plaintext.

Inspect the destination before taking ownership of existing files, show the proposed diff, and ask
before the first `chezmoi apply`.

## Add the work overlay

Follow [Work overlay](./work-overlay.md) for the isolated personal chezmoi invocation, combined
wrapper, aliases, bootstrap order, and verification commands.

The resulting command surface is:

| Command | Personal source | Work source |
| --- | --- | --- |
| `cz` | Pull/status | Pull/status |
| `cz apply` | Apply first | Apply second |
| `cz update` | Update first | Update second |
| `czp …` | Run only here | — |
| `czw …` | — | Run only here |

On a personal machine, `cz` remains the ordinary single-repo wrapper; `czp` and `czw` are only
needed on layered work machines.
