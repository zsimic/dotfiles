#!/bin/zsh

set -euf

typeset -r script_dir="${0:A:h}"
typeset -r action="${1:-}"
typeset -r work_only="${WORK_ONLY:-}"
typeset -r personal_wrapper="$script_dir/chezmoi-personal.sh"
typeset -r status_helper="$HOME/bin/gremlins/check-repo-status"

run_personal() {
    [[ -n "$work_only" ]] || "$personal_wrapper" "$@"
}

case "$action" in
    "")
        run_personal
        PULL=1 TITLE=work "$status_helper" "$script_dir"
        chezmoi status
        ;;
    fetch)
        [[ -n "$work_only" ]] || "$personal_wrapper" fetch
        TITLE=work "$status_helper" "$script_dir"
        ;;
    pull)
        [[ -n "$work_only" ]] || "$personal_wrapper" pull
        PULL=1 TITLE=work "$status_helper" "$script_dir"
        ;;
    apply|diff|managed|status|unmanaged|update)
        if [[ -z "$work_only" ]]; then
            echo "---- personal $action: ----"
            "$personal_wrapper" "$@"
            echo "---- work $action: ----"
        fi
        chezmoi "$@"
        ;;
    *)
        if [[ -n "$work_only" ]]; then
            chezmoi "$@"
        else
            print -u2 "Command '$action' is not enabled for the combined setup"
            exit 1
        fi
        ;;
esac
