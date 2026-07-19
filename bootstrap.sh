#!/bin/zsh

# Bootstrap chezmoi
# zsh -c "$(curl -fsSL https://raw.githubusercontent.com/zsimic/dotfiles/main/bootstrap.sh)"

set -eufx
typeset -U path
path=(/opt/homebrew/bin /home/linuxbrew/.linuxbrew/bin $path)

if ! command -v brew > /dev/null; then
    if [[ "$OSTYPE" == darwin* ]]; then
        echo "Homebrew's initial macOS installation requires an administrator password."
        /usr/bin/sudo -v
    fi
    NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    for folder in $path[1,2]; do
        if [ -x "$folder/brew" ]; then
            eval "$($folder/brew shellenv)"
            break
        fi
    done
fi

if ! command -v chezmoi > /dev/null; then
    HOMEBREW_NO_ENV_HINTS=1 HOMEBREW_NO_INSTALL_CLEANUP=1 brew install chezmoi
fi

if [[ "$USER" == "zoran" ]]; then
    chezmoi init --apply zsimic
fi
