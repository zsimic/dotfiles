#!/usr/bin/env bash
# source by interactive shells (keep compatible with bash and zsh)

[ -n "$MAILCHECK" ] && unset MAILCHECK
[ -z "$TERMINFO_DIRS" ] && export TERMINFO_DIRS=/usr/share/terminfo

export RIPGREP_CONFIG_PATH="$HOME/.config/ripgrep/config"
export PYTHON_HISTORY="$HOME/.local/state/history/python.history"

alias cz="$HOME/.local/share/chezmoi/cz.sh"

if command -v eza > /dev/null; then
    alias ls='eza -F --color-scale --time-style iso'
else
    alias ls='ls -GFh --color=auto'
fi

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
alias wget='wget --hsts-file="$HOME/.local/share/wget-hsts"'

mptree() {
    for name in "$@"; do
        if [ "$name" -eq "$name" ]; then
            pstree -g3 -p "$name" | grep --color=auto -E "($name|$)"
            echo
        else
            echo "⋯⋯ $name ⋯⋯" | grep --color=auto "⋯"
            for pid in $(pgrep -i $name); do
                pstree -g3 -p "$pid" | grep --color=auto -E "($pid|$name|$)"
                echo
            done
        fi
    done
}

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

[ -r "$HOME/.local/aliases" ] && . "$HOME/.local/aliases"

if [ -d "$HOME/.sdkman/bin" ]; then
    export SDKMAN_DIR="$HOME/.sdkman"
    . "$SDKMAN_DIR/bin/sdkman-init.sh"
fi

# Minimalistic shell prompt
__ps1s="$HOME/bin/shrinky.py"
__l_ps1h=""
_update_custom_prompt() {
    local ps1h=( -c$__shell -ozsimic,zoran -p"$PWD" -u$USER -v"$VIRTUAL_ENV" -x$? )
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
