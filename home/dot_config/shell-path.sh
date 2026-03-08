#!/bin/sh
# sourced by all shells that need PATH, keep compatible with bash and zsh

# This repo has a fixed structure and would be irrelevant for any other XDG layout, we still define entries in standard way
: "${XDG_CACHE_HOME:=$HOME/.cache}"
: "${XDG_CONFIG_HOME:=$HOME/.config}"
: "${XDG_DATA_HOME:=$HOME/.local/share}"
: "${XDG_STATE_HOME:=$HOME/.local/state}"

cleanup_path() {  # Dedupe and cleanup entries from a PATH-like value that point to non-existing folders
    echo -n "$1" | awk -vRS=: '(!a[$0]++){if(system("test -d \""$0"\"")==0){if(b++)printf(RS);printf($0)}}'
}

prepend_path() {
    [ -d "$1" ] && PATH="$1:$PATH"
}

PATH=$(cleanup_path "$PATH")
if [ -z "$HOMEBREW_PREFIX" ]; then
    # Probe brew directly, as we have a chicken and egg conundrum (brew needed on PATH in order to call `brew shellenv`...)
    if [ -x /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [ -x /home/linuxbrew/.linuxbrew/bin/brew ]; then
        eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    fi
fi

prepend_path "$HOME/.local/bin"
prepend_path "$HOME/.cargo/bin"

PATH=$(cleanup_path "$PATH")
export PATH

# Keep the bootstrap helper namespace clean
unset -f prepend_path # cleanup_path
