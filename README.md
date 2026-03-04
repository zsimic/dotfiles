# Zoran's dotfiles

My dotfiles, managed with [chezmoi](https://github.com/twpayne/chezmoi).

# CLIs

- [bat](https://github.com/sharkdp/bat) - A `cat(1)` clone with wings
- [btop](https://github.com/aristocratos/btop) - Resource monitor
- [curlie](https://github.com/rs/curlie) - The power of curl, the ease of use of httpie
- [dua-cli](https://github.com/Byron/dua-cli) - Like `du`, but better
- [duf](https://github.com/muesli/duf) - Disk Usage/Free utility - a better `df` alternative
- [eza](https://github.com/eza-community/eza) - Modern alternative to `ls`
- [fd](https://github.com/sharkdp/fd) - Fast and user-friendly alternative to `find`
- [fzf](https://github.com/junegunn/fzf) - Command-line fuzzy finder
- [git-delta](https://github.com/dandavison/delta) - Syntax-highlighting pager for git, diff, grep, and blame output
- [htop](https://htop.dev/) - Interactive process viewer
- [ripgrep](https://github.com/BurntSushi/ripgrep) - `grep` on steroids
- [tmux](https://github.com/tmux/tmux) - Terminal multiplexer
- [tokei](https://github.com/XAMPPRocky/tokei) - Count lines of code in a project
- [tre-command](https://github.com/dduan/tre) - Like `tree`, but way better
- [wget](https://www.gnu.org/software/wget/) - Good ol' GNU web get
- [zoxide](https://github.com/ajeetdsouza/zoxide) - Smarter `cd` command

Not automated:

- [grpcurl](https://github.com/fullstorydev/grpcurl) - Like cURL, but for gRPC

# Terminals

- [ghostty](https://ghostty.org/) - My current daily-driver terminal emulator
- [iterm2](https://iterm2.com/) - Previous classic


# Ghostty

- Default config: `ghostty +show-config --default --docs > ghostty-default.conf`
- http://shadertoy.com/
- https://github.com/linkarzu/dotfiles-latest/tree/main/ghostty/shaders


# Seldom used

- https://github.com/sharkdp/hyperfine
- https://dev.yorhel.nl/ncdu
- https://github.com/bensadeh/tailspin
- https://github.com/imsnif/bandwhich


# Tests

Some scripts have [tests](./tests), run `tox` to exercise the tests.
`tox -e venv` can be used to conveniently get a `.venv/`.
