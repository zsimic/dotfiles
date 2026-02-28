# Zoran's dotfiles

Zoran's dotfiles, managed with [chezmoi](https://github.com/twpayne/chezmoi).

```shell
chezmoi init git@github.com:zsimic/dotfiles.git
```


# Terminals

- https://ghostty.org/
- https://iterm2.com/


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
