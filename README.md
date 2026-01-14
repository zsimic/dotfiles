# Zoran's dotfiles

Currently trying `chezmoi`, it has some nice sides, but it is trying to use
naming conventions as file permission management...
Open/looking for alternatives, ideal utility would be simpler and not
overcomplicate things with file permissions.

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
