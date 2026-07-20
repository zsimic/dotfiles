# Automated tools

This is a readable inventory of the current desired state. The linked
[Rust manager](../../home/bin/gremlins/executable_manage-rust-tools) and
[Brewfile](../../home/dot_config/homebrew/Brewfile) are authoritative.

## Rust CLIs

Installed with `cargo-binstall`; package names that differ from their primary executable are shown explicitly.

| Tool | Cargo package | Use |
| --- | --- | --- |
| [atuin](https://github.com/atuinsh/atuin) | `atuin` | Searchable, SQLite-backed shell history |
| [bat](https://github.com/sharkdp/bat) | `bat` | `cat` with syntax highlighting and paging |
| [dua](https://github.com/Byron/dua-cli) | `dua-cli` | Interactive disk-usage inspection |
| [eza](https://github.com/eza-community/eza) | `eza` | Modern `ls` replacement |
| [fd](https://github.com/sharkdp/fd) | `fd-find` | Fast, friendly `find` replacement |
| [delta](https://github.com/dandavison/delta) | `git-delta` | Syntax-aware pager for Git and diffs |
| [ripgrep](https://github.com/BurntSushi/ripgrep) | `ripgrep` | Fast recursive text search; executable is `rg` |
| [tokei](https://github.com/XAMPPRocky/tokei) | `tokei` | Source-code statistics |
| [tre](https://github.com/dduan/tre) | `tre-command` | Tree view with sensible ignores |
| [xh](https://github.com/ducaale/xh) | `xh` | Friendly HTTP client |
| [zoxide](https://github.com/ajeetdsouza/zoxide) | `zoxide` | Frecency-based directory jumping |

## Homebrew formulae

| Tool | Use |
| --- | --- |
| [btop](https://formulae.brew.sh/formula/btop) | Interactive resource monitor |
| [duf](https://formulae.brew.sh/formula/duf) | Disk usage/free summary |
| [pstree](https://formulae.brew.sh/formula/pstree) | Process hierarchy display |
| [tmux](https://formulae.brew.sh/formula/tmux) | Terminal multiplexer |

## macOS casks

Chezmoi installs or adopts missing casks without upgrading existing ones. Monthly maintenance leaves
self-updating casks to their own updaters and upgrades only casks that do not declare `auto_updates`.

Installed on every macOS target:

| Cask | Use |
| --- | --- |
| [1Password](https://formulae.brew.sh/cask/1password) | Password manager |
| [Symbols Only Nerd Font][symbols-font] | Icon glyphs for terminal prompts and tools |
| [Ghostty](https://formulae.brew.sh/cask/ghostty) | Primary terminal emulator |
| [Google Chrome](https://formulae.brew.sh/cask/google-chrome) | Browser |
| [iTerm2](https://formulae.brew.sh/cask/iterm2) | Retained terminal emulator |
| [Pearcleaner](https://formulae.brew.sh/cask/pearcleaner) | Application uninstaller and cleanup tool |
| [Shottr](https://formulae.brew.sh/cask/shottr) | Screenshot utility |
| [Sublime Text](https://formulae.brew.sh/cask/sublime-text) | Text editor |
| [Raycast](https://formulae.brew.sh/cask/raycast) | Launcher and productivity tool |

[symbols-font]: https://formulae.brew.sh/cask/font-symbols-only-nerd-font

Additionally installed for the `zoran` account:

| Cask | Use |
| --- | --- |
| [Discord](https://formulae.brew.sh/cask/discord) | Chat |
| [Firefox](https://formulae.brew.sh/cask/firefox) | Browser |
| [IINA](https://formulae.brew.sh/cask/iina) | Media player |
| [OnyX](https://formulae.brew.sh/cask/onyx) | macOS maintenance utility |
| [QuickLook Video][quicklook-video] | Quick Look support for more video formats |

[quicklook-video]: https://formulae.brew.sh/cask/quicklook-video
