#!/bin/zsh -ef

ensure_folders() {
    for folder in "$@"; do
        [ -d "$folder" ] || mkdir -p "$folder"
    done
}

ensure_folders "$HOME/.local/bin" "$HOME/.local/config" "$HOME/.local/state/history"
ensure_folders "$HOME/.cache/zsh" "$HOME/.local/share/zsh/site-functions"
if [[ -n "$CODER" || -d /Users ]]; then
    ensure_folders "$HOME/dev" "$HOME/github" "$HOME/tmp"
fi
