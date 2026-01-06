#!/bin/bash

set -e

_TMUX_EXE=/opt/homebrew/bin/tmux
SESSION_NAME=${1:-main}
RUNC=
if [ "$1" = "debug" ]; then
    SESSION_NAME=demo
    RUNC=echo
    set -x
elif [ -n "$TMUX" ]; then
    echo "Already in tmux"
    exit 0
fi

if ! $_TMUX_EXE has-session -t $SESSION_NAME 2> /dev/null; then
    $RUNC $_TMUX_EXE new-session -d -s $SESSION_NAME -c ~
    if [ -f ~/.config/tmux.$SESSION_NAME.cfg ]; then
        for ss in $(cat ~/.config/tmux.$SESSION_NAME.cfg | sed "s#~#$HOME#"); do
            sleep 0.0001
            $RUNC $_TMUX_EXE new-window -c $ss
        done
    fi
fi
exec $RUNC $_TMUX_EXE attach-session -t $SESSION_NAME
