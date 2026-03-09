#!/bin/zsh -eufx

[ -x "/Library/Developer/CommandLineTools/usr/bin/git" ] || xcode-select --install
#[ -f "/Library/Apple/usr/share/rosetta/rosetta" ] || softwareupdate --install-rosetta --agree-to-license
