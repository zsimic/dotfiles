# Zoran's dotfiles

My dotfiles, managed with [chezmoi](https://github.com/twpayne/chezmoi).

# CLIs

Rust CLIs managed via [cargo binstall](home/bin/gremlins/executable_manage-rust-tools).

- [atuin](https://github.com/atuinsh/atuin) - Shell history in sqlite
- [bat](https://github.com/sharkdp/bat) - A `cat(1)` clone with wings
- [dua](https://github.com/Byron/dua-cli) - Like `du`, but better
- [eza](https://github.com/eza-community/eza) - Modern alternative to `ls`
- [fd](https://github.com/sharkdp/fd) - Fast and user-friendly alternative to `find`
- [git-delta](https://github.com/dandavison/delta) - Syntax-highlighting pager for git, diff, grep, and blame output
- [ripgrep](https://github.com/BurntSushi/ripgrep) - `grep` on steroids
- [tokei](https://github.com/XAMPPRocky/tokei) - Count lines of code in a project
- [tre](https://github.com/dduan/tre) - Like `tree`, but way better
- [xh](https://github.com/ducaale/xh) - Friendly and fast tool for sending HTTP requests
- [zoxide](https://github.com/ajeetdsouza/zoxide) - Smarter `cd` command

Not automated (or seldom used):

- [bandwhich](https://github.com/imsnif/bandwhich) - Terminal bandwidth utilization tool
- [dust](https://github.com/bootandy/dust) - A more intuitive version of `du` in Rust; Cargo package is `du-dust`
- [hyperfine](https://github.com/sharkdp/hyperfine) - Command-line benchmarking tool
- [tailspin](https://github.com/bensadeh/tailspin) - Log file highlighter; executable is `tspin`
- [uv](https://github.com/astral-sh/uv) - An extremely fast Python package and project manager, written in Rust

Managed with brew.

- [btop](https://github.com/aristocratos/btop) _(C++)_ - Resource monitor
- [duf](https://github.com/muesli/duf) _(go)_ - Disk Usage/Free utility - a better `df` alternative
- [tmux](https://github.com/tmux/tmux) _(C)_ - Terminal multiplexer

Other/older used in the past:

- [curlie](https://github.com/rs/curlie) _(go)_ - The power of curl, the ease of use of httpie
- [grpcurl](https://github.com/fullstorydev/grpcurl) _(go)_ - Like cURL, but for gRPC
- [htop](https://htop.dev/) _(C)_ - Interactive process viewer
- [ncdu](https://dev.yorhel.nl/ncdu) _(C)_ - Ncurses Disk Usage

# Terminals

- [ghostty](https://ghostty.org/) _(zig)_ - My current daily-driver terminal emulator
- [iTerm2](https://iterm2.com/) _(Objective-C)_  - Previous classic

# Ghostty

- Default config: `ghostty +show-config --default --docs > ghostty-default.conf`
- http://shadertoy.com/
- https://github.com/linkarzu/dotfiles-latest/tree/main/ghostty/shaders

# Tests

Some scripts have [tests](./tests), run `tox` to exercise the tests.
`tox -e venv` can be used to conveniently get a `.venv/`.
