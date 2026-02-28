#!/bin/zsh

typeset -U path
path+=(/opt/homebrew/bin)
path+=(/home/linuxbrew/.linuxbrew/bin)

if ! command -v brew > /dev/null; then
    NONINTERACTIVE=1 bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    hash -r
    brew install chezmoi
fi
