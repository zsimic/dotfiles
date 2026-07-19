# Tools

This section is the human-readable inventory of software managed or considered by this repository. The linked source files remain authoritative; these pages explain the choices and lifecycle around them.

- [Automated](./automated.md) — Rust CLIs, Homebrew formulae, and macOS casks installed by chezmoi.
- [Exploratory](./exploratory.md) — useful tools that are not currently part of the automated desired state.
- [Rust tool management](./rust.md) — how `cargo-binstall`, the install hook, and monthly upgrades fit together.
- [Terminals](./terminals.md) — the Ghostty-first setup, tmux session launcher, and retained iTerm2 configuration.

Sources of truth:

- [`manage-rust-tools`](../../home/bin/gremlins/executable_manage-rust-tools)
- [`Brewfile`](../../home/dot_config/homebrew/Brewfile)
- [chezmoi lifecycle scripts](../../home/.chezmoiscripts/)
