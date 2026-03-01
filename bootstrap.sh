#!/usr/bin/env zsh

# Bootstrap chezmoi
# zsh -c "$(curl -fsSL https://raw.githubusercontent.com/zsimic/dotfiles/refs/heads/main/bootstrap.sh)"

typeset -U path
path+=(/opt/homebrew/bin)
path+=(/home/linuxbrew/.linuxbrew/bin)

if ! command -v chezmoi > /dev/null; then
    if ! command -v brew > /dev/null; then
        NONINTERACTIVE=1 $SHELL -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        hash -r
    fi
    brew install chezmoi
fi

if [[ "$USER" == "zoran" ]]; then
    chezmoi init --apply zsimic
fi
