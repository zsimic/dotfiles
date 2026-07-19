# Zoran's dotfiles

A compact, public-safe [chezmoi](https://www.chezmoi.io/) source state for a consistent shell and
tool setup across macOS and Linux. It is deliberately framework-free: zsh is the daily shell, bash
remains a supported peer, and shared settings stay in ordinary shell files.

[Documentation](./docs/index.md) · [Reuse this setup](./docs/reuse/index.md) ·
[Tool inventory](./docs/tools/index.md) · [Fresh-machine checklist](./docs/bootstrap.md)

## What is interesting here

- Bash and zsh share their PATH and most interactive settings through
  [`shell-path.sh`](./home/dot_config/shell-path.sh) and
  [`shell-settings.sh`](./home/dot_config/shell-settings.sh).
- System tools and macOS applications live in a checked-in, condition-aware
  [`Brewfile`](./home/dot_config/homebrew/Brewfile); the resulting inventory is documented under
  [Tools](./docs/tools/index.md).
- Rust CLIs are installed with `cargo-binstall`, including a Linux musl fallback for binaries with
  newer glibc requirements; see [Rust tool management](./docs/tools/rust.md).
- Chezmoi `run_onchange_` hooks keep side effects tied to the files that drive them instead of
  running a general provisioning pass on every apply; see the
  [development conventions](./docs/dev/index.md).
- The repository intentionally contains no secrets or machine-specific credentials.

## Daily workflow

[`cz.sh`](./cz.sh) is a small wrapper around chezmoi:

```console
cz          # pull and show pending changes
cz fetch    # check the remote
cz apply    # apply the source state
cz update   # pull and apply
```

## Layout

- [`home/`](./home/) — chezmoi source state, lifecycle scripts, and managed configuration.
- [`bootstrap.sh`](./bootstrap.sh) — installs Homebrew and chezmoi, then applies this repository.
- [`resources/`](./resources/) — source material used by managed configuration.
- [`tests/`](./tests/) — tests for the non-trivial helpers; run `tox` and `tox -e style`.
- [`docs/`](./docs/) — concise operational documentation.
