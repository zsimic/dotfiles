#!/bin/zsh

set -euf

typeset -r action="${1:-}"
typeset -r personal_root="$HOME/.local/share/pd"
typeset -r personal_source="$personal_root/personal-dotfiles"
typeset -r personal_config="$personal_root/chezmoi.toml"
typeset -r personal_cache="$personal_root/cache"
typeset -r personal_state="$personal_root/state.boltdb"
typeset -r status_helper="$HOME/bin/gremlins/check-repo-status"

personal_chezmoi() {
    chezmoi \
        --source "$personal_source" \
        --config "$personal_config" \
        --cache "$personal_cache" \
        --persistent-state "$personal_state" \
        "$@"
}

case "$action" in
    "")
        PULL=1 TITLE=personal "$status_helper" "$personal_source"
        personal_chezmoi status
        ;;
    fetch)
        TITLE=personal "$status_helper" "$personal_source"
        ;;
    pull)
        PULL=1 TITLE=personal "$status_helper" "$personal_source"
        ;;
    init)
        mkdir -p "$personal_cache"
        personal_chezmoi --config-path "$personal_config" "$@"
        ;;
    *)
        personal_chezmoi "$@"
        ;;
esac
