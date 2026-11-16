# Tools

This section is the human-readable inventory of software managed or considered by this repository.
The linked source files remain authoritative; these pages explain the choices and lifecycle around
them.

- [Automated](./automated.md) — Homebrew formulae and macOS casks installed by chezmoi, plus their lifecycle.
- [Exploratory](./exploratory.md) — useful tools that are not currently part of the automated desired state.
- [Python maintenance](./python.md) — upgrade uv-managed Pythons and remove superseded stable patches.
- [Terminals](./terminals.md) — the Ghostty-first setup, tmux session launcher, and retained iTerm2
  configuration.

Sources of truth:

- [`Brewfile`](../../home/dot_config/homebrew/Brewfile)
- [chezmoi lifecycle scripts](../../home/.chezmoiscripts/)
