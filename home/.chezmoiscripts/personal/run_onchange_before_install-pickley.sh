#!/bin/zsh -euf

[ -d /srv ] && exit 0

if [[ ! -x  ~/.local/bin/pickley ]]; then
    zsh -c "$(curl -fsSL https://raw.githubusercontent.com/codrsquad/pickley/main/get-pickley)"
fi
 ~/.local/bin/pickley install mgit
