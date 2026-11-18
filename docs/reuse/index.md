# Reuse this setup

For someone who wants the same shape: a small, public-safe personal dotfiles base for home machines,
which can also sit underneath a private work layer, with no framework, just two chezmoi sources applied
in order. Written for the coding agent doing the adapting: enough to take it from there, as inspiration
rather than a package to install. The [README](../../README.md) says what is worth reusing.

> Suggested prompt: "Read `docs/reuse/index.md` from `github.com/zsimic/dotfiles` and help me adapt
> this setup for my own personal and work environments. Ask for the missing repository URLs and
> preferences before changing files or applying anything."

Keep the architecture, pick your own tools from the [inventory](../tools/index.md). Don't run the
bootstrap unchanged: it only applies this source state on my personal machines. A fork replaces my
identity: the personal-machine gates, the repo in [`bootstrap.sh`](../../bootstrap.sh), and the
[git config](../../home/dot_config/git/config) name and email.

## Two shapes

- **Personal machines**: the personal repo is the normal chezmoi source at `~/.local/share/chezmoi`;
  the standard bootstrap and `cz` wrapper are enough.
- **Work machines**: the private work repo takes `~/.local/share/chezmoi`, the personal repo is cloned
  with its own config, cache, and state, and a work wrapper applies personal first, then work. See
  [Work overlay](./work-overlay.md).

This is ordered application, not file-level merging: keep target files disjoint. If both repos manage
the same target, the work version wins, but the personal repo keeps reporting it as changed.

## Extension points

The personal base owns the stable parent configuration and optionally loads a file the work repo owns.
Use the same pattern for new integration points:

| Work-owned target | Loaded by | Purpose |
| --- | --- | --- |
| `~/.local/shell-path.sh` | [shell-path] | Work-only PATH and environment |
| `~/.local/aliases.sh` | [shell-settings] | Work-only aliases and functions |
| `~/.config/git/config-work` | [git-config] | Work identity, hosts, and Git behavior |
| `agents/[0-9]*.md` in the work repo | [agents.md] | Work notes for coding agents |

[shell-path]: ../../home/dot_config/shell-path.sh
[shell-settings]: ../../home/dot_config/shell-settings.sh
[git-config]: ../../home/dot_config/git/config
[agents.md]: ../agents.md

## Before changing anything

An assistant helping with this asks first:

1. Fork of this repo, or a new repo using it as a reference?
2. Personal and work Git URLs, and which are private?
3. Operating systems and usernames to support?
4. Which tools and applications from the inventory to automate?
5. Which work-only files are needed, and do they fit the extension points?
6. Where secrets live (never as plaintext in either source state)?

Then it inspects existing destination files before taking them over, shows the proposed diff, and asks
before the first `chezmoi apply`.
