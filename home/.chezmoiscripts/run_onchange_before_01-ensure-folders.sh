#!/usr/bin/env zsh

set -e

ensure_folders() {
    for folder in "$@"; do
        [ -d "$folder" ] || mkdir -p "$folder"
    done
}

ensure_folders ~/dev ~/github ~/tmp ~/.local/bin ~/.local/state/zsh/completions
