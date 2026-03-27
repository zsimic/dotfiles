#!/bin/zsh

# Small wrapper around chezmoi, adding some subcommands

set -e

ACTION="$1"

if [[ -z "$ACTION" ]]; then
    PULL=1 "$HOME/bin/gremlins/check-repo-status" "$HOME/.local/share/chezmoi"
    chezmoi status

elif [[ "$ACTION" = "fetch" ]]; then
    "$HOME/bin/gremlins/check-repo-status" "$HOME/.local/share/chezmoi"

elif [[ "$ACTION" = "pull" ]]; then
    PULL=1 "$HOME/bin/gremlins/check-repo-status" "$HOME/.local/share/chezmoi"

else
    chezmoi "$@"

fi
