# Documentation

This repository is a small, public-safe chezmoi source state for keeping a mostly shared bash and
zsh environment, selected tool configuration, and macOS applications consistent across machines.
These notes assume familiarity with dotfiles and use this page as the map;
the [chezmoi documentation](https://www.chezmoi.io/) covers the underlying tool.

## Sections and guides

- [Bootstrap](./bootstrap.md) — ordered, copy-pasteable checklist for a fresh machine and interrupted-run recovery.
- [Tools](./tools/index.md) — automated and exploratory tool inventories, Rust installation lifecycle, and terminal setup.
- [Development](./dev/index.md) — repository design, working conventions, tests, and how to adapt the pattern.
- [Repository overview](../README.md) — the design choices, daily workflow, and important entry points.

## Source map

- [`home/`](../home/) — managed home-directory state; macOS-only lifecycle scripts are under `home/.chezmoiscripts/darwin/`.
- [`bootstrap.sh`](../bootstrap.sh) — fresh-machine entry point.
- [`cz.sh`](../cz.sh) — daily chezmoi wrapper.
- [`tests/`](../tests/) — automated tests for Python helpers and shell-facing utilities.
