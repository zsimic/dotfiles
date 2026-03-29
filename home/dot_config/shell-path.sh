# sourced by all shells that need PATH, keep compatible with bash and zsh
# This repo has a fixed structure and would be irrelevant for any other XDG layout, we still define entries in standard way
: "${XDG_CACHE_HOME:=$HOME/.cache}"
: "${XDG_CONFIG_HOME:=$HOME/.config}"
: "${XDG_DATA_HOME:=$HOME/.local/share}"
: "${XDG_STATE_HOME:=$HOME/.local/state}"
export XDG_CACHE_HOME
export XDG_CONFIG_HOME
export XDG_DATA_HOME
export XDG_STATE_HOME

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

        [[ -n "$part" && -d "$part" ]] || continue

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

append_path() {
    if [ -d "$1" ]; then
        case ":$PATH:" in
            *":$1:"*) return ;;
        esac
        PATH="$PATH:$1"
    fi
}

prepend_path() {
    if [ -d "$1" ]; then
        PATH="$1:$PATH"
    fi
}

append_path "/usr/local/bin"
append_path "$HOME/Library/Application Support/JetBrains/Toolbox/scripts"

if [ -z "${SDKMAN_DIR:-}" ] && [ -d "$HOME/.sdkman/bin" ]; then
    export SDKMAN_DIR="$HOME/.sdkman"
    . "$SDKMAN_DIR/bin/sdkman-init.sh"
fi

for brew_folder in /opt/homebrew /home/linuxbrew/.linuxbrew; do
    if [[ -d "$brew_folder" ]]; then
        prepend_path "$brew_folder/sbin"
        prepend_path "$brew_folder/bin"
    fi
done
unset brew_folder

prepend_path "$HOME/.local/bin"
prepend_path "$HOME/.cargo/bin"
prepend_path "$HOME/bin"

# less setup done via env vars because older less versions don't respect XDG...
export LESSHISTFILE="$HOME/.local/state/lesshst"
export LESS="-SFWJ --no-histdups --mouse --wheel-lines=3"

# Optional machine-specific additions
if [ -r "$HOME/.local/shell-path.sh" ]; then
    . "$HOME/.local/shell-path.sh"
fi

PATH=$(cleanup_path "$PATH")
