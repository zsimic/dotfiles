#!/bin/zsh

# Small wrapper around chezmoi, adding a `fetch` command

ACTION="$1"

if [[ "$ACTION" == (f|fetch) ]]; then
    exec ~/bin/check-repo-status ~/.local/share/chezmoi
fi

if [[ "$ACTION" == (p|pull) ]]; then
    exec chezmoi git pull
fi

exec chezmoi "$@"
