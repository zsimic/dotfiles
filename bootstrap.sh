#!/bin/zsh

# Bootstrap chezmoi
# zsh -c "$(curl -fsSL https://raw.githubusercontent.com/zsimic/dotfiles/main/bootstrap.sh)"

BREW_PATHS=(/opt/homebrew/bin /home/linuxbrew/.linuxbrew/bin)
typeset -U path
path+=($BREW_PATHS)

if ! command -v brew > /dev/null; then
    NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    for brew_bin in $BREW_PATHS; do
        if [[ -x "$brew_bin/brew" ]]; then
            eval "$($brew_bin/brew shellenv)"
            break
        fi
    done
fi

if ! command -v chezmoi > /dev/null; then
    brew install chezmoi
fi

if [[ "$USER" == "zoran" ]]; then
    chezmoi init --apply zsimic
fi
