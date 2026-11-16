# Automated tools

This is a readable inventory of the current desired state. The [Brewfile] is authoritative.
See [exploratory] for more tools mentions.

[Brewfile]: ../../home/dot_config/homebrew/Brewfile
[exploratory]: ./exploratory.md

## Homebrew formulae

| Tool | Language | Use |
| --- | --- | --- |
| [atuin] | Rust | Searchable, SQLite-backed shell history |
| [bat] | Rust | `cat` with syntax highlighting and paging |
| [btop] | C++ | Interactive resource monitor |
| [dua-cli] | Rust | Interactive disk-usage inspection |
| [duf] | Go | Disk usage/free summary |
| [eza] | Rust | Modern `ls` replacement |
| [fd] | Rust | Fast, friendly `find` replacement |
| [git-delta] | Rust | Syntax-aware pager for Git and diffs; executable is `delta` |
| [jaq] | Rust | `jq` clone focused on speed and correctness |
| [pstree] | C | Process hierarchy display |
| [ripgrep] | Rust | Fast recursive text search; executable is `rg` |
| [tmux] | C | Terminal multiplexer |
| [tokei] | Rust | Source-code statistics |
| [tre-command] | Rust | Tree view with sensible ignores |
| [xh] | Rust | Friendly HTTP client |
| [zoxide] | Rust | Frecency-based directory jumping |

Additionally installed on a subset of personal machines:

| Tool | Language | Use |
| --- | --- | --- |
| [container] | Swift | Run Linux containers in lightweight VMs on macOS only |
| [uv] | Rust | Python package and project management |

[atuin]: https://github.com/atuinsh/atuin
[bat]: https://github.com/sharkdp/bat
[btop]: https://github.com/aristocratos/btop
[container]: https://github.com/apple/container
[dua-cli]: https://github.com/Byron/dua-cli
[duf]: https://github.com/muesli/duf
[eza]: https://github.com/eza-community/eza
[fd]: https://github.com/sharkdp/fd
[git-delta]: https://github.com/dandavison/delta
[jaq]: https://github.com/01mf02/jaq
[pstree]: https://github.com/FredHucht/pstree
[ripgrep]: https://github.com/BurntSushi/ripgrep
[tmux]: https://github.com/tmux/tmux
[tokei]: https://github.com/XAMPPRocky/tokei
[tre-command]: https://github.com/dduan/tre
[uv]: https://github.com/astral-sh/uv
[xh]: https://github.com/ducaale/xh
[zoxide]: https://github.com/ajeetdsouza/zoxide

## macOS casks

Chezmoi installs or adopts missing casks without upgrading existing ones. Monthly maintenance leaves
self-updating casks to their own updaters and upgrades only casks that do not declare `auto_updates`.

Installed on every macOS target:

| Cask | Language | Use |
| --- | --- | --- |
| [AppCleaner] | Unverified | Application uninstaller and cleanup tool |
| [Symbols Only Nerd Font][symbols-font] | N/A (font) | Icon glyphs for terminal prompts and tools |
| [Ghostty] | [Zig, Swift][ghostty-source] | Primary terminal emulator |
| [Google Chrome][chrome] | C++ (Chromium core) | Browser |
| [iTerm2] | [Objective-C][iterm-source] | Retained terminal emulator |
| [Shottr] | Swift | Screenshot utility |
| [Sublime Text][sublime] | C++ | Text editor |
| [Raycast] | Rust+others | Launcher and productivity tool |

[AppCleaner]: https://formulae.brew.sh/cask/appcleaner
[symbols-font]: https://formulae.brew.sh/cask/font-symbols-only-nerd-font
[Ghostty]: https://formulae.brew.sh/cask/ghostty
[ghostty-source]: https://github.com/ghostty-org/ghostty
[chrome]: https://formulae.brew.sh/cask/google-chrome
[iTerm2]: https://formulae.brew.sh/cask/iterm2
[iterm-source]: https://github.com/gnachman/iTerm2
[Shottr]: https://formulae.brew.sh/cask/shottr
[sublime]: https://formulae.brew.sh/cask/sublime-text
[Raycast]: https://formulae.brew.sh/cask/raycast

Additionally installed on a subset of personal machines:

| Cask | Language | Use |
| --- | --- | --- |
| [1Password] | Rust, React | Password manager |
| [Discord] | React | Chat |
| [Firefox] | C++, Rust, JavaScript | Browser |
| [IINA] | [Swift][iina-source] | Media player |
| [OnyX] | Objective-C | macOS maintenance utility |
| [QuickLook Video][quicklook-video] | [Swift, Objective-C][quicklook-source] | Quick Look video support |

[1Password]: https://formulae.brew.sh/cask/1password
[Discord]: https://formulae.brew.sh/cask/discord
[Firefox]: https://formulae.brew.sh/cask/firefox
[IINA]: https://formulae.brew.sh/cask/iina
[iina-source]: https://github.com/iina/iina
[OnyX]: https://formulae.brew.sh/cask/onyx
[quicklook-video]: https://formulae.brew.sh/cask/quicklook-video
[quicklook-source]: https://github.com/Marginal/QuickLookVideo

## Apply and monthly maintenance

The shared [brew.env] applies to manual Homebrew commands and chezmoi maintenance. This setup exports
`XDG_CONFIG_HOME=$HOME/.config`, so Homebrew reads `~/.config/homebrew/brew.env` automatically.
It hides environment hints, leaves casks declaring `auto_updates` to their own updaters, and defers
automatic install/upgrade cleanup to the explicit monthly cleanup step. Manual `brew upgrade` follows
these same defaults; use `--greedy-auto-updates` to include self-updating casks explicitly, and
`brew cleanup` to clean up between monthly runs. Only the automation scripts set `HOMEBREW_NO_ASK`,
preserving normal confirmation prompts for manual commands. See [Homebrew's environment documentation].

Other shared defaults disable analytics, highlight `brew cat` output with `bat`, quiet automatic update
reports, and show formula installation times. `brew install` leaves already-installed packages at their
current versions; use `brew upgrade` to update them.

The [brew install hook] includes the Brewfile's hash, so it runs on the first apply and whenever the
inventory changes. Existing packages are left at their installed versions during this step.

The [monthly hook] renders the current year and month into the script. The first `chezmoi apply` in
a new month runs [monthly-upgrade] to update Homebrew, upgrade packages, and clean old artifacts.
It runs `brew autoremove` for unused formula dependencies, then standard `brew cleanup` to remove old
installed versions and stale downloads. Cache retention is set to 60 days: aged downloads are removed
on the next cleanup after that threshold, while obsolete downloads can be removed sooner.
This is apply-driven, not a background scheduler. Run it explicitly with:

```zsh
~/bin/gremlins/monthly-upgrade
```

[brew install hook]: ../../home/.chezmoiscripts/run_onchange_after_02-install-brew-tools.sh.tmpl
[monthly hook]: ../../home/.chezmoiscripts/run_onchange_after_90-monthly-upgrade.sh.tmpl
[monthly-upgrade]: ../../home/bin/gremlins/executable_monthly-upgrade
[brew.env]: ../../home/dot_config/homebrew/brew.env
[Homebrew's environment documentation]: https://docs.brew.sh/Manpage#environment
