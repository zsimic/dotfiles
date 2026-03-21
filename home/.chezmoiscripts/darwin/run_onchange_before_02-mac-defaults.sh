#!/bin/zsh -euf

# Avoid creating .DS_Store files on network or USB volumes
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
defaults write com.apple.desktopservices DSDontWriteUSBStores -bool true

# Finder
defaults write com.apple.finder NewWindowTarget -string "PfHm"
defaults write com.apple.finder NewWindowTargetPath -string "file://${HOME}/"
defaults write com.apple.finder ShowStatusBar -bool true
defaults write com.apple.finder ShowPathbar -bool true
defaults write com.apple.finder WarnOnEmptyTrash -bool false
defaults write com.apple.finder FXRemoveOldTrashItems -bool true

# Screenshots to ${HOME}/Pictures/
defaults write com.apple.screencapture location -string "${HOME}/Pictures/"
defaults write com.apple.screencapture name -string "ScreenShot"
defaults write com.apple.screencapture show-thumbnail -bool false

# dock settings
defaults write com.apple.dock tilesize -int 30
defaults write com.apple.dock recent-apps -array ""

# Fast keyboard repeat rate
defaults write NSGlobalDomain AppleShowAllExtensions -bool true  # Show all filename extensions
defaults write NSGlobalDomain KeyRepeat -int 2
defaults write NSGlobalDomain InitialKeyRepeat -int 15

# iterm2
defaults write com.googlecode.iterm2 PromptOnQuit -bool false
defaults write com.googlecode.iterm2 LoadPrefsFromCustomFolder -bool true
defaults write com.googlecode.iterm2 PrefsCustomFolder "$CHEZMOI_WORKING_TREE/resources/darwin/iterm2/"

##defaults write com.googlecode.iterm2 NoSyncNeverRemindPrefsChangesLostForFile_Path -string "$CHEZMOI_WORKING_TREE/resources/darwin/iterm2/com.googlecode.iterm2.plist"
#defaults write com.googlecode.iterm2 NoSyncNeverRemindPrefsChangesLostForFile -bool true
#defaults write com.googlecode.iterm2 NoSyncNeverRemindPrefsChangesLostForFile_selection -int 2
#defaults write com.googlecode.iterm2 NoSyncTipsDisabled -bool true
