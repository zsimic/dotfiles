#!/bin/zsh -ef

ensure_folders() {
    for folder in "$@"; do
        [ -d "$folder" ] || mkdir -p "$folder"
    done
}

ensure_folders ~/.cache/zsh ~/.local/bin ~/.local/config ~/.local/share/zsh/site-functions ~/.local/state/history
ensure_folders ~/dev ~/github ~/tmp
