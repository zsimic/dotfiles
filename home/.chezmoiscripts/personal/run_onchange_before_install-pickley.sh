#!/bin/zsh -eufx

[ -d /srv ] && exit 0

if [[ ! -x  "$HOME/.local/bin/pickley" ]]; then
    zsh -c "$(curl -fsSL https://raw.githubusercontent.com/codrsquad/pickley/main/get-pickley)"
fi
"$HOME/.local/bin/pickley" install mgit
