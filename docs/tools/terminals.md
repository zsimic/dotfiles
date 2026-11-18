# Terminals

[Ghostty](https://ghostty.org/) is the primary terminal; [iTerm2](https://iterm2.com/) is kept as a
configured alternative. Both are macOS-only, excluded elsewhere by
[`.chezmoiignore`](../../home/.chezmoiignore).

## Ghostty

The main [Ghostty config] starts [join-tmux] with the `main` session; the helper creates or attaches it,
opens its configured working-directory windows, and keeps terminal-specific sessions apart. Ghostty
keeps one line of scrollback because tmux owns scrollback.

[demo.conf] and [scratch.conf] are alternate profiles; [zterm] opens a named profile in a clean
environment (`zterm demo`), or an iTerm2 profile with `zterm i <profile>`.

`ghostty +show-config --default --docs` prints every option with its default; see also the
[configuration reference](https://ghostty.org/docs/config) and [example shaders][shader-examples].

[Ghostty config]: ../../home/dot_config/ghostty/config
[join-tmux]: ../../home/bin/executable_join-tmux
[demo.conf]: ../../home/dot_config/ghostty/demo.conf
[scratch.conf]: ../../home/dot_config/ghostty/scratch.conf
[zterm]: ../../home/bin/executable_zterm
[shader-examples]: https://github.com/linkarzu/dotfiles-latest/tree/main/ghostty/shaders

## iTerm2

The macOS defaults hook points iTerm2's custom preferences folder at the checked-in
[iTerm2 preferences]; a dedicated `run_onchange_` hook restarts iTerm2 when that file changes.

[iTerm2 preferences]: ../../resources/darwin/iterm2/com.googlecode.iterm2.plist
