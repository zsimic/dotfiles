# zsh / bash compatible custom settings

# Interactive shells only, no need for scipts (in case tthi gets sourced by mistake)
[[ $- != *i* ]] && return 0

[ -n "$MAILCHECK" ] && unset MAILCHECK
[ -z "$TERMINFO_DIRS" ] && export TERMINFO_DIRS=/usr/share/terminfo

# prepend_to_path() { [ -d "$1" ] && export PATH=$1:$PATH; }
append_to_path() { [ -d "$1" ] && export PATH=$PATH:$1; }

append_to_path ~/.local/bin
append_to_path /opt/homebrew/bin
append_to_path ~/.cargo/bin

# remove duplicates in PATH (but keep order)
export PATH=$(echo -n $PATH | awk -vRS=: '(!a[$0]++){if(system("test -d \""$0"\"")==0){if(b++)printf(RS);printf($0)}}')
#export PATH="$(echo -n $PATH | awk -v RS=: '(!a[$0]++){if(b++)printf(RS);printf($0)}')"

if command -v eza > /dev/null; then
    alias ls='eza -F --color-scale --time-style iso'
    alias l='ls -la'
else
    alias ls='ls -GFh --color=auto'
    alias l='ls -lA'
fi

# export UV_INDEX_URL=https://pypi.netflix.net/simple
alias honesty='~/github/honesty/.venv/bin/honesty'

export RIPGREP_CONFIG_PATH=~/.config/ripgrep.conf

command -v bat > /dev/null && { export MANPAGER="sh -c 'col -bx | bat -l man -p'"; alias less=bat; }
command -v batcat > /dev/null && { export MANPAGER="sh -c 'col -bx | batcat -l man -p'"; alias less=batcat; }
if command -v dua > /dev/null; then alias du='dua'; else alias du='du -sh'; fi
if command -v duf > /dev/null; then alias df='duf'; else alias df='df -h'; fi
if command -v fdfind > /dev/null; then alias fd='fdfind --hidden'; elif command -v fd > /dev/null; then alias fd='fd --hidden'; fi
if command -v tre > /dev/null; then alias tree='tre'; fi
if command -v tspin > /dev/null; then alias tail='tspin'; fi
alias zpickley='~/github/pickley/.venv/bin/pickley'
alias zpp='~/github/portable-python/.venv/bin/portable-python'
alias zrunez='~/github/runez/.venv/bin/python -mrunez'
alias homelab-srv=~/github/homelab-srv/.venv/bin/homelab-srv
#alias ag='rg'
alias ll='ls -l'
alias la='ls -la'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'

if [[ -d ~/dev/newt ]]; then
    upynt() {
        PYNT_USE_UV=1 ~/dev/nfpy/pynt/.venv/bin/pynt "$@"
    }
    alias zick='~/github/ick/.venv/bin/ick'
    alias zpynt='~/dev/nfpy/pynt/.venv/bin/pynt'
    alias znfty='~/dev/nfpy/nfty/.venv/bin/nfty'
    alias zgrpc='~/dev/nfpy/nflx-grpc/.venv/bin/nflx-grpc'
    alias zpc='newt --app-type python pycharm open'
    znewt() { NEWT_CONFIGS_DIR=~/dev/newt/newt-configs newt "$@"; }
fi

edit() {
    local s="/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl"
    [ -x "$s" ] && { "$s" "$@" ; return $?; }
    nano "$@"
}
_fgw() { local g; for g in ./gradlew ../gradlew ../../gradlew; do [ -f "$g" ] && { echo -n "$g"; return 0; }; done; }
g() { local g=$(_fgw); [ -x "$g" ] && { echo $g "$@"; $g "$@"; } || { echo "No gradlew found"; return 1; }; }
tailf() {
    command -v bat > /dev/null && { tail -f "$@" | bat --paging=never -l log; return $?; }
    tail -f "$@"
}
psgrep() { ( ps aux | head -n 1; ps aux | grep -v grep | grep --color=always "${@:-tmux}" ) | /usr/bin/less -SFR; }
zz() {  # Toggle python venv
    [ -n "$VIRTUAL_ENV" ] && { deactivate; return $?; }
    [ ! -d .venv ] && { echo "No .venv folder"; return 1; }
    [ ! -f .venv/bin/activate ] && { echo ".venv was not successfully built"; return 1; }
    source .venv/bin/activate
}

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

if [ -f "$__ps1s" ]; then
    if [ -n "$ZSH_VERSION" ]; then
        __shell="zsh"; precmd() { _update_custom_prompt; }
    elif [ -n "$BASH_VERSION" ]; then
        __shell="bash"; PROMPT_COMMAND="_update_custom_prompt"
    fi
fi
