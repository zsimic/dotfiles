#!/bin/zsh

# Small wrapper around chezmoi, adding some subcommands

set -e

ACTION="$1"

if [[ -z "$ACTION" ]]; then
    if ! PULL=1 ~/bin/check-repo-status ~/.local/share/chezmoi; then
        exec chezmoi status
    fi

elif [[ "$ACTION" = "fetch" ]]; then
    exec ~/bin/check-repo-status ~/.local/share/chezmoi

elif [[ "$ACTION" = "pull" ]]; then
    exec chezmoi git pull

else
    exec chezmoi "$@"

fi
