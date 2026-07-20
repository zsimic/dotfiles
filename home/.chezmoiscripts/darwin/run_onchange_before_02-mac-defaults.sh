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

# Use F1, F2, etc. as standard function keys
defaults write NSGlobalDomain com.apple.keyboard.fnState -bool true

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

# Disable unwanted macOS keyboard shortcuts
disabled_hotkeys=(
    52          # Dock: Turn Dock hiding on/off

    32 34       # Mission Control: Mission Control and its slow-animation variant
    33 35       # Mission Control: Application windows and its slow-animation variant
    36 37       # Mission Control: Show Desktop and its slow-animation variant
    79 80 81 82 # Mission Control: Move left/right a Space and their slow-animation variants
    {118..133}  # Mission Control: Switch to Desktop 1–16
    163         # Mission Control: Show Notification Center
    175         # Mission Control: Turn Do Not Disturb on/off
    190         # Mission Control: Quick Note
    222         # Mission Control: Stage Manager
    260         # Mission Control: Game Overlay

    233 235     # Windows / General: Minimize and Zoom
    237 238 239 # Windows / General: Fill, Center, and Return to Previous Size
    {240..243}  # Windows / Halves: Tile left, right, top, and bottom
    {244..247}  # Windows / Quarters: Tile into each quarter
    {248..251}  # Windows / Arrange: Arrange two windows along either axis
    256         # Windows / Arrange: Arrange in Quarters
    257 258     # Windows / Full Screen Tile: Tile left and right

    13          # Keyboard: Change the way Tab moves focus
    12          # Keyboard: Turn keyboard access on or off
    7           # Keyboard: Move focus to the menu bar
    8           # Keyboard: Move focus to the Dock
    9           # Keyboard: Move focus to active or next window
    10          # Keyboard: Move focus to the window toolbar
    11          # Keyboard: Move focus to the floating window
    # 27        # Keyboard: Move focus to next window ⌘` (kept enabled)
    57          # Keyboard: Move focus to status menus
    159         # Keyboard: Show contextual menu

    {28..31}    # Screenshots: Capture the screen or selection to a file or the clipboard
    184         # Screenshots: Screenshot and recording options
    181 182     # Screenshots: Capture the Touch Bar to a file or the clipboard

    223 224     # Presenter Overlay: Turn the large or small overlay on or off

    64 65       # Spotlight: Show Spotlight search and Finder search

    25 26       # Accessibility / Contrast: Increase and decrease contrast
    21          # Accessibility: Reverse black and white
    {215..219}  # Accessibility / Live Captions: All shortcuts
    {225..229}  # Accessibility / Live Speech: All shortcuts
    230 231 232 # Accessibility: Speak selection, pointer item, and typing feedback
    162         # Accessibility: Show Accessibility controls
    59          # Accessibility: Turn VoiceOver on or off
    15 17 19 23 179 # Accessibility / Zoom: All keyboard shortcuts
)
for hotkey in "${disabled_hotkeys[@]}"; do
    defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add "$hotkey" '<dict><key>enabled</key><false/></dict>'
done

# Reload keyboard shortcut settings in the current session
shortcut_activator="/System/Library/PrivateFrameworks/SystemAdministration.framework/Resources/activateSettings"
if [[ -x "$shortcut_activator" ]]; then
    "$shortcut_activator" -u
fi
