#!/bin/zsh

# Small wrapper around chezmoi, adding some subcommands

set -e

ACTION="$1"

if [[ -z "$ACTION" ]]; then
    PULL=1 ~/bin/check-repo-status ~/.local/share/chezmoi
    chezmoi status

elif [[ "$ACTION" = "fetch" ]]; then
    ~/bin/check-repo-status ~/.local/share/chezmoi

elif [[ "$ACTION" = "pull" ]]; then
    PULL=1 ~/bin/check-repo-status ~/.local/share/chezmoi

else
    chezmoi "$@"

fi
