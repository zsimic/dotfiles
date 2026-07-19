# Terminals

[Ghostty](https://ghostty.org/) is the primary terminal; [iTerm2](https://iterm2.com/) is retained as
a configured alternative. The terminal configuration is macOS-only and is excluded elsewhere by
[`.chezmoiignore`](../../home/.chezmoiignore).

## Ghostty

The main [Ghostty config] starts [join-tmux] with the `main` session. The helper creates or attaches
the session, opens its configured working-directory windows, and keeps terminal-specific sessions
separate.

[Ghostty config]: ../../home/dot_config/ghostty/config
[join-tmux]: ../../home/bin/executable_join-tmux

Notable choices in the main profile:

- JetBrains Mono, a dark `Deep`-based palette, a background image, and the `hot-cursor` shader.
- One line of Ghostty scrollback because tmux owns scrollback.
- `Cmd-R` reloads the configuration.
- macOS Option acts as Alt; terminal key sequences are explicit where shell/readline behavior differs.
- Clipboard paste protection remains enabled.

[demo.conf] and [scratch.conf] are focused alternate profiles. [zterm] opens named profiles in a
clean environment; for example:

[demo.conf]: ../../home/dot_config/ghostty/demo.conf
[scratch.conf]: ../../home/dot_config/ghostty/scratch.conf
[zterm]: ../../home/bin/executable_zterm

```zsh
zterm demo
zterm scratch
```

Useful Ghostty references:

- [Configuration reference](https://ghostty.org/docs/config)
- Inspect the installed defaults: `ghostty +show-config --default --docs > ghostty-default.conf`
- [Shadertoy](https://www.shadertoy.com/) and [example terminal shaders][shader-examples]

[shader-examples]: https://github.com/linkarzu/dotfiles-latest/tree/main/ghostty/shaders

## iTerm2

The checked-in [iTerm2 preferences] file is configured as iTerm2's custom preferences folder by the
macOS defaults hook. A dedicated `run_onchange_` hook restarts iTerm2 when that source file changes.

[iTerm2 preferences]: ../../resources/darwin/iterm2/com.googlecode.iterm2.plist

`zterm i <profile>` opens one of the named iTerm2 profiles, while `zterm <profile>` targets Ghostty.
