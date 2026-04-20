# Zoran's dotfiles

My dotfiles, managed with [chezmoi](https://github.com/twpayne/chezmoi).


# CLIs

- [atuin](https://github.com/atuinsh/atuin) _(rust)_ - Shell history in sqlite
- [bat](https://github.com/sharkdp/bat) _(rust)_ - A `cat(1)` clone with wings
- [btop](https://github.com/aristocratos/btop) _(C++)_ - Resource monitor
- [curlie](https://github.com/rs/curlie) _(go)_ - The power of curl, the ease of use of httpie
- [dua-cli](https://github.com/Byron/dua-cli) _(rust)_ - Like `du`, but better
- [duf](https://github.com/muesli/duf) _(go)_ - Disk Usage/Free utility - a better `df` alternative
- [eza](https://github.com/eza-community/eza) _(rust)_ - Modern alternative to `ls`
- [fd](https://github.com/sharkdp/fd) _(rust)_ - Fast and user-friendly alternative to `find`
- [git-delta](https://github.com/dandavison/delta) _(rust)_ - Syntax-highlighting pager for git, diff, grep, and blame output
- [ripgrep](https://github.com/BurntSushi/ripgrep) _(rust)_ - `grep` on steroids
- [tmux](https://github.com/tmux/tmux) _(C)_ - Terminal multiplexer
- [tokei](https://github.com/XAMPPRocky/tokei) _(rust)_ - Count lines of code in a project
- [tre-command](https://github.com/dduan/tre) _(rust)_ - Like `tree`, but way better
- [zoxide](https://github.com/ajeetdsouza/zoxide) _(rust)_ - Smarter `cd` command

Not automated:

- [grpcurl](https://github.com/fullstorydev/grpcurl) _(go)_ - Like cURL, but for gRPC
- [htop](https://htop.dev/) _(C)_ - Interactive process viewer


# Terminals

- [ghostty](https://ghostty.org/) _(zig)_ - My current daily-driver terminal emulator
- [iTerm2](https://iterm2.com/) _(Objective-C)_  - Previous classic


# Ghostty

- Default config: `ghostty +show-config --default --docs > ghostty-default.conf`
- http://shadertoy.com/
- https://github.com/linkarzu/dotfiles-latest/tree/main/ghostty/shaders


# Seldom used

- https://github.com/sharkdp/hyperfine _(rust)_ - Command-line benchmarking tool
- https://dev.yorhel.nl/ncdu _(C)_ - Ncurses Disk Usage
- https://github.com/bensadeh/tailspin _(rust)_ - Log file highlighter
- https://github.com/imsnif/bandwhich _(rust)_ - Terminal bandwidth utilization tool


# Tests

Some scripts have [tests](./tests), run `tox` to exercise the tests.
`tox -e venv` can be used to conveniently get a `.venv/`.
