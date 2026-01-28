# zsh / bash compatible custom settings

# Interactive shells only, not needed for scripts (in case this gets sourced by mistake)
[[ $- != *i* ]] && return 0

[ -n "$MAILCHECK" ] && unset MAILCHECK
[ -z "$TERMINFO_DIRS" ] && export TERMINFO_DIRS=/usr/share/terminfo

append_to_path() { [ -d "$1" ] && export PATH=$PATH:$1; }

append_to_path ~/.local/bin
append_to_path /opt/homebrew/bin
append_to_path /home/linuxbrew/.linuxbrew/bin
append_to_path ~/.cargo/bin

if command -v eza > /dev/null; then
    alias ls='eza -F --color-scale --time-style iso'
else
    alias ls='ls -GFh --color=auto'
fi

export RIPGREP_CONFIG_PATH=~/.config/ripgrep.conf

if command -v bat > /dev/null; then
    export MANPAGER="sh -c 'col -bx | bat -l man -p'"
    alias less=bat
elif command -v batcat > /dev/null; then
    export MANPAGER="sh -c 'col -bx | batcat -l man -p'"
    alias less=batcat
fi

if command -v dua > /dev/null; then alias du='dua'; else alias du='du -sh'; fi
if command -v duf > /dev/null; then alias df='duf'; else alias df='df -h'; fi
if command -v fdfind > /dev/null; then alias fd='fdfind --hidden'; elif command -v fd > /dev/null; then alias fd='fd --hidden'; fi
if command -v tre > /dev/null; then alias tree='tre'; fi
alias ll='ls -l'
alias la='ls -lA'
alias l='ls -lA'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'

edit() {
    local s="/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl"
    [ -x "$s" ] && { "$s" "$@" ; return $?; }
    nano "$@"
}
zz() {  # Toggle python venv
    [ -n "$VIRTUAL_ENV" ] && { deactivate; return $?; }
    [ ! -d .venv ] && { echo "No .venv folder"; return 1; }
    [ ! -r .venv/bin/activate ] && { echo ".venv was not successfully built"; return 1; }
    . .venv/bin/activate
}

[ -r ~/.local/aliases ] && . ~/.local/aliases

if [ -d ~/.sdkman/bin ]; then
    export SDKMAN_DIR="$HOME/.sdkman"
    . "$SDKMAN_DIR/bin/sdkman-init.sh"
fi

# Minimalistic shell prompt
__ps1s=~/bin/shrinky.py
_update_custom_prompt() {
    local ps1h=( -s$__shell -w$TMUX_PANE -u$USER -x$? -ozsimic,zoran -p"$PWD" -v"$VIRTUAL_ENV" )
    [[ "${ps1h[@]}" == "$__l_ps1h" ]] && return;
    local v=$(/usr/bin/python3 $__ps1s ps1 "${ps1h[@]}")
    [ -z "$v" ] && return;
    PS1=$v
    __l_ps1h="${ps1h[@]}"
    if [[ -n "$TMUX_PANE" && "$__l_pwd" != "$PWD" ]]; then  # Change tmux window name
        __l_pwd=$PWD
        printf '\033k%s\033\\' $(/usr/bin/python3 $__ps1s tmux_short -p"$PWD")
    fi
}

if [ -r "$__ps1s" ]; then
    if [ -n "$ZSH_VERSION" ]; then
        __shell="zsh"; precmd() { _update_custom_prompt; }
    elif [ -n "$BASH_VERSION" ]; then
        __shell="bash"; PROMPT_COMMAND="_update_custom_prompt"
    fi
fi
