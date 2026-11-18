# Automated tools

A readable overview of the tools in use, for a mental map; the [Brewfile] is the source of truth, and
its gates decide which machines get what (the icons below only hint at it).

New tools are usually added to the Brewfile by hand, in the right gate: that choice is only verifiable by
applying on several machines. Agents help keep these tables in sync with it, spot drift, and discuss
candidates (see [exploratory]).

[Brewfile]: ../../home/dot_config/homebrew/Brewfile
[exploratory]: ./exploratory.md

## Homebrew formulae

👤: mostly on personal machines

| Tool | Language | Use |
| --- | --- | --- |
| [atuin] | Rust | Searchable, SQLite-backed shell history |
| [bat] | Rust | `cat` with syntax highlighting and paging |
| [btop] | C++ | Interactive resource monitor |
| [container] 👤 | Swift | Linux containers in lightweight VMs on macOS only |
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
| [uv] 👤 | Rust | Python package and project management |
| [zoxide] | Rust | Frecency-based directory jumping |

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

🔄: updated through Homebrew, as the cask doesn't declare `auto_updates` (check with
`brew info --json=v2 --cask <name>`)

| Cask | Language | Use |
| --- | --- | --- |
| [1Password] 👤 | Rust, React | Password manager |
| [AppCleaner] | Objective-C | Application uninstaller and cleanup tool |
| [Discord] 👤 | React | Chat |
| [Firefox] 👤 | C++, Rust, JavaScript | Browser |
| [Ghostty] | Zig, Swift | Primary terminal emulator |
| [Google Chrome] | C++ (Chromium core) | Browser |
| [IINA] 👤 | Swift | Media player |
| [iTerm2] | Objective-C | Retained terminal emulator |
| [OnyX] 👤🔄 | Objective-C | macOS maintenance utility |
| [QuickLook Video] 👤🔄 | Swift, Objective-C | Quick Look video support |
| [Raycast] | React, Rust, Swift | Launcher and productivity tool |
| [Shottr] | Swift | Screenshot utility |
| [Sublime Text] | C++ | Text editor |
| [Nerd Font] 🔄 | - | Icon glyphs for terminal prompts and tools |

[1Password]: https://1password.com/
[AppCleaner]: https://freemacsoft.net/appcleaner/
[Discord]: https://discord.com/
[Firefox]: https://www.mozilla.org/firefox/
[Ghostty]: https://github.com/ghostty-org/ghostty
[Google Chrome]: https://www.google.com/chrome/
[IINA]: https://github.com/iina/iina
[iTerm2]: https://github.com/gnachman/iTerm2
[OnyX]: https://www.titanium-software.fr/en/onyx.html
[QuickLook Video]: https://github.com/Marginal/QuickLookVideo
[Raycast]: https://raycast.com/
[Shottr]: https://shottr.cc/
[Sublime Text]: https://www.sublimetext.com/
[Nerd Font]: https://github.com/ryanoasis/nerd-fonts

## Apply and monthly maintenance

- Homebrew reads [brew.env] on its own (this setup exports `XDG_CONFIG_HOME=$HOME/.config`), so its
  defaults apply to manual commands and automation alike; the file comments each setting.
- The [brew install hook] embeds the Brewfile's hash: it runs on first apply and whenever the inventory
  changes, installing what is missing without upgrading anything.
- The [monthly hook] renders the current month, so the first apply of each month runs
  [monthly-upgrade] (update, upgrade, autoremove, cleanup). It is apply-driven, not scheduled; run it
  by hand any time.
- Only the automation sets `HOMEBREW_NO_ASK`, so manual commands keep their prompts. Casks declaring
  `auto_updates` are left to their own updaters; `brew upgrade --greedy-auto-updates` includes them.

[brew install hook]: ../../home/.chezmoiscripts/run_onchange_after_02-install-brew-tools.sh.tmpl
[monthly hook]: ../../home/.chezmoiscripts/run_onchange_after_90-monthly-upgrade.sh.tmpl
[monthly-upgrade]: ../../home/bin/gremlins/executable_monthly-upgrade
[brew.env]: ../../home/dot_config/homebrew/brew.env
