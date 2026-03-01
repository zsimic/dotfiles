#!/usr/bin/env zsh

set -e

if [[ ! -x "/Library/Developer/CommandLineTools/usr/bin/git" ]]; then
    xcode-select --install
fi

if [[ ! -f "/Library/Apple/usr/share/rosetta/rosetta" ]]; then
    softwareupdate --install-rosetta --agree-to-license
fi
