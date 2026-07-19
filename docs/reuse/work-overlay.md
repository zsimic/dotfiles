# Work overlay

This page contains the copyable scaffold for applying a shared personal chezmoi source before a
private work source. Read [Reuse this setup](./index.md) first for the ownership model and extension
points.

## Layout

On a work machine, keep the work repo in chezmoi's default location and isolate the personal
invocation under a separate root:

```text
~/.local/share/chezmoi/             # private work source; default chezmoi state
├── .chezmoiroot
├── chezmoi-personal.sh
├── cz.sh
└── home/

~/.local/share/pd/
├── personal-dotfiles/              # shared personal source
├── chezmoi.toml
├── cache/
└── state.boltdb
```

The exact secondary root is a local convention; change it consistently if `~/.local/share/pd` is
not appropriate.

## Personal wrapper

Place this executable `chezmoi-personal.sh` beside `cz.sh` in the work repo. The separate source,
config, cache, and persistent-state paths prevent the two chezmoi invocations from sharing
bookkeeping.

```zsh
#!/bin/zsh

set -euf

typeset -r action="${1:-}"
typeset -r personal_root="$HOME/.local/share/pd"
typeset -r personal_source="$personal_root/personal-dotfiles"
typeset -r personal_config="$personal_root/chezmoi.toml"
typeset -r personal_cache="$personal_root/cache"
typeset -r personal_state="$personal_root/state.boltdb"
typeset -r status_helper="$HOME/bin/gremlins/check-repo-status"

personal_chezmoi() {
    chezmoi \
        --source "$personal_source" \
        --config "$personal_config" \
        --cache "$personal_cache" \
        --persistent-state "$personal_state" \
        "$@"
}

case "$action" in
    "")
        PULL=1 TITLE=personal "$status_helper" "$personal_source"
        personal_chezmoi status
        ;;
    fetch)
        TITLE=personal "$status_helper" "$personal_source"
        ;;
    pull)
        PULL=1 TITLE=personal "$status_helper" "$personal_source"
        ;;
    init)
        mkdir -p "$personal_cache"
        personal_chezmoi --config-path "$personal_config" "$@"
        ;;
    *)
        personal_chezmoi "$@"
        ;;
esac
```

The status helper is this repo's [check-repo-status]. It always fetches and, with `PULL=1`, rebases
a clean repo that is behind its upstream. Replace those calls with ordinary
`git -C … fetch/status/pull` commands if the helper is not part of the personal base.

[check-repo-status]: ../../home/bin/gremlins/executable_check-repo-status

## Combined work wrapper

The work repo's `cz.sh` owns the combined command surface. It permits a conservative set of
commands across both sources; `WORK_ONLY=1` passes any other command directly to the work
invocation.

```zsh
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
    apply|diff|init|managed|status|unmanaged|update)
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
```

Keep both helpers executable in Git:

```zsh
chmod +x chezmoi-personal.sh cz.sh
```

## Work-only aliases

The personal base already defines `cz` as `~/.local/share/chezmoi/cz.sh`. On a work machine that
path resolves to the combined wrapper above. Add only the scoped aliases to the work-owned
`~/.local/aliases.sh`:

```zsh
alias czp="$HOME/.local/share/chezmoi/chezmoi-personal.sh"
alias czw='WORK_ONLY=1 "$HOME/.local/share/chezmoi/cz.sh"'
```

## First setup on a work machine

Clone the work source without applying it, initialize and apply the personal base, then inspect and
apply the work overlay:

```zsh
work_repo_url="git@github.com:your-company/work-dotfiles.git"
personal_repo_url="https://github.com/you/dotfiles.git"

chezmoi init "$work_repo_url"
"$HOME/.local/share/chezmoi/chezmoi-personal.sh" init --apply "$personal_repo_url"
chezmoi diff
chezmoi apply
exec zsh -l
```

This order ensures the personal base has installed `check-repo-status` before the combined wrapper
needs it. If the work source uses a configuration template, answer its prompts during
`chezmoi init`; it still does not update `$HOME` until the final apply.

## Verify

```zsh
czp status
czw status
cz status
cz diff
```

`cz diff` should show the personal diff first and the work diff second. After reviewing it,
`cz apply` preserves that same order.
