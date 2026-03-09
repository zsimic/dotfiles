#!/bin/bash
# sourced by all shells that need PATH, keep compatible with bash and zsh

# This repo has a fixed structure and would be irrelevant for any other XDG layout, we still define entries in standard way
: "${XDG_CACHE_HOME:=$HOME/.cache}"
: "${XDG_CONFIG_HOME:=$HOME/.config}"
: "${XDG_DATA_HOME:=$HOME/.local/share}"
: "${XDG_STATE_HOME:=$HOME/.local/state}"

cleanup_path() {  # Dedupe and cleanup entries from a PATH-like value that point to non-existing folders
    local input=$1
    local output=
    local seen=
    local part

    while [ -n "$input" ]; do
        part=${input%%:*}
        if [ "$input" = "$part" ]; then
            input=
        else
            input=${input#*:}
        fi

        [ -z "$part" ] && continue
        [ -d "$part" ] || continue

        case ":$seen:" in
            *":$part:"*) ;;
            *)
                seen="${seen:+$seen:}$part"
                output="${output:+$output:}$part"
                ;;
        esac
    done

    printf '%s' "$output"
}

append_path() { [ -d "$1" ] && PATH="$PATH:$1"; }
prepend_path() { [ -d "$1" ] && PATH="$1:$PATH"; }

PATH=$(cleanup_path "$PATH")

append_path "$HOME/Library/Application Support/JetBrains/Toolbox/scripts"

# Probe brew directly, as we have a chicken and egg conundrum (brew needed on PATH in order to call `brew shellenv`...)
if [ -z "$HOMEBREW_PREFIX" ]; then
    for folder in /opt/homebrew /home/linuxbrew/.linuxbrew; do
        if [ -x "$folder/bin/brew" ]; then
            eval "$($folder/bin/brew shellenv)"
            break
        fi
    done
fi

prepend_path "$HOME/.local/bin"
prepend_path "$HOME/.cargo/bin"

export PATH=$(cleanup_path "$PATH")
