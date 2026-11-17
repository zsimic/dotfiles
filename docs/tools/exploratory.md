# Exploratory tools

Useful tools that are not currently part of the automated desired state. Handy list of possible
candidates to move to [automated] (or vice versa).

[automated]: ./automated.md

## Candidates

| Tool | Language | Use |
| --- | --- | --- |
| [bandwhich] | Rust | Per-process terminal bandwidth monitor |
| [dust] | Rust | More intuitive disk usage |
| [hyperfine] | Rust | Command-line benchmarking |
| [tailspin] | Rust | Log highlighting; executable is `tspin` |

[bandwhich]: https://github.com/imsnif/bandwhich
[dust]: https://github.com/bootandy/dust
[hyperfine]: https://github.com/sharkdp/hyperfine
[tailspin]: https://github.com/bensadeh/tailspin

## Previous or occasional tools

†: Removed by [brew install hook]

| Tool | Language | Use |
| --- | --- | --- |
| [curlie] † | Go | Curl-compatible HTTP client with an HTTPie-like interface |
| [fzf] †| Go | Command-line fuzzy finder |
| [grpcurl] | Go | Command-line client for gRPC services |
| [htop] | C | Interactive process viewer |
| [less] †| C | Terminal text pager |
| [ncdu] | Zig | Ncurses disk-usage browser |
| [the_silver_searcher] † | C | Fast source-code search; executable is `ag` |
| [wget] † | C | Command-line file downloader |

[curlie]: https://github.com/rs/curlie
[fzf]: https://github.com/junegunn/fzf
[grpcurl]: https://github.com/fullstorydev/grpcurl
[htop]: https://htop.dev/
[less]: https://github.com/gwsw/less
[ncdu]: https://dev.yorhel.nl/ncdu
[the_silver_searcher]: https://github.com/ggreer/the_silver_searcher
[wget]: https://www.gnu.org/software/wget/

[brew install hook]: ../../home/.chezmoiscripts/run_onchange_after_02-install-brew-tools.sh.tmpl
