#!/bin/zsh -e

# Use custom folder for iTerm2 prefs
defaults write com.googlecode.iterm2 PrefsCustomFolder -string ~/.config/iterm2
defaults write com.googlecode.iterm2 LoadPrefsFromCustomFolder -bool true
defaults write com.googlecode.iterm2 NoSyncNeverRemindPrefsChangesLostForFile_Path -string ~/.config/iterm2/com.googlecode.iterm2.plist

defaults write NSGlobalDomain KeyRepeat -int 2
defaults write NSGlobalDomain InitialKeyRepeat -int 15
