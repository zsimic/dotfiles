# Set up your own dotfiles with chezmoi + a `cz` wrapper

> **This page is written for an AI coding assistant (Claude Code, etc.).**
> **Human:** open your assistant in a fresh session and say something like:
> *"Read `docs/getting-started.md` from `github.com/zsimic/dotfiles` and help me set up the same
> dotfiles system for myself."*
> The assistant should follow the steps below, asking you for your details as it goes.

## What you're building

A reproducible dev environment managed by [chezmoi](https://www.chezmoi.io/): your shell,
aliases, editor, and tool configs live in a git repo and apply to any machine with one
command. A tiny wrapper, `cz`, gives you a friction-free pull → review → apply workflow.

**Reference implementation** — read it as you work; mirror its conventions:
<https://github.com/zsimic/dotfiles>

## Guardrails (read first)

- **Never commit secrets** (tokens, API keys, passwords) — this repo is likely public.
- **Ask the user before** editing their shell config or running `chezmoi apply`.
- Prefer copying the reference repo's structure over inventing a new one.

## Steps

### 1. Install chezmoi

See <https://www.chezmoi.io/install/>. Then `chezmoi init` to start (or clone) a dotfiles repo.

### 2. Track your dotfiles

`chezmoi add ~/.zshrc ~/.config/<tool>/...` for each thing you want versioned. chezmoi stores
them in a source repo (naming convention: `dot_zshrc` → `~/.zshrc`). Commit and push.

### 3. Add the `cz` wrapper + alias

A small `cz.sh` makes daily use effortless. Copy the pattern from the reference repo's
[`cz.sh`](https://github.com/zsimic/dotfiles/blob/main/cz.sh):

```sh
cz          # pull + show what's pending
cz fetch    # check the remote for changes
cz apply    # apply (passes through to chezmoi)
cz update   # pull + apply
```

And the alias, in your shell config (so it's the same on every machine):
```sh
alias cz="$HOME/.local/share/chezmoi/cz.sh"
```

### 4. One-command bootstrap

A `bootstrap.sh` that installs chezmoi (plus any prereqs) and inits your repo means a
brand-new machine is **one command** away from fully configured. See the reference
[`bootstrap.sh`](https://github.com/zsimic/dotfiles/blob/main/bootstrap.sh).

## Going further: a thin private (or work) layer

Have config that *shouldn't* live in a public repo — machine-specific bits, or work-only
settings that name internal hosts/services? Add a **second, private** repo as a thin layer on
top of this one, and keep this public repo free of any private details.

A small wrapper applies the personal repo first, then the private layer on top, all under the
same `cz` command — so you get one workflow everywhere, with personal and private cleanly
separated. (If your employer publishes an internal version of this guide, point your assistant
at that too — it'll set up the private half the same way.)

## Done

`cz` shows what's pending, `cz apply` lays it down, `cz update` does both. Your setup now
travels with you to every machine.


# Example `cz.sh` wrapper for a work-side setup

As work-only aliases:

```shell
alias czp="$HOME/.local/share/chezmoi/chezmoi-personal.sh"
alias czw='WORK_ONLY=1 "$HOME/.local/share/chezmoi/cz.sh"'
```

Helper `chezmoi-personal.sh` script (this script is like running `chezmoi` scoped to the
personal dotfiles part only):

```shell
ACTION="$1"
DOTFILES="$HOME/.local/share/pd"

p_chezmoi() {
    chezmoi --source "$DOTFILES/personal-dotfiles" \
            --config "$DOTFILES/chezmoi.toml" \
            --cache "$DOTFILES/tmp" \
            --persistent-state "$DOTFILES/state.boltdb" \
            "$@"
}

if [[ -z "$ACTION" ]]; then
    PULL=1 TITLE=personal "$HOME/bin/gremlins/check-repo-status" "$DOTFILES/personal-dotfiles"
    p_chezmoi status

elif [[ "$ACTION" = "fetch" ]]; then
    TITLE=personal "$HOME/bin/gremlins/check-repo-status" "$DOTFILES/personal-dotfiles"

elif [[ "$ACTION" = "pull" ]]; then
    PULL=1 TITLE=personal "$HOME/bin/gremlins/check-repo-status" "$DOTFILES/personal-dotfiles"

elif [[ "$ACTION" == (auto-init|remove|reset) ]]; then
    if [[ "$ACTION" == (remove|reset) ]]; then
        rm -rf "$DOTFILES"
    fi
    if [[ "$ACTION" != "remove" && ! -d "$DOTFILES/personal-dotfiles"  ]]; then
        mkdir -p "$DOTFILES/tmp"
        echo "Personal dotfiles wrapper" > "$DOTFILES/README.md"
        url=...  # Point to your personal chezmoi
        p_chezmoi --config-path "$DOTFILES/chezmoi.toml" init $url
    fi

else
    p_chezmoi "$@"

fi
```

Work-side `cz.sh`:

```shell
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
ACTION="$1"

if [[ -z "$ACTION" ]]; then
    [[ -z "$WORK_ONLY" ]] && "$SCRIPT_DIR/chezmoi-personal.sh"
    PULL=1 TITLE=work "$HOME/bin/gremlins/check-repo-status" "$SCRIPT_DIR"
    chezmoi status

elif [[ "$ACTION" = "fetch" ]]; then
    [[ -z "$WORK_ONLY" ]] && "$SCRIPT_DIR/chezmoi-personal.sh" fetch
    TITLE=work "$HOME/bin/gremlins/check-repo-status" "$SCRIPT_DIR"

elif [[ "$ACTION" = "pull" ]]; then
    [[ -z "$WORK_ONLY" ]] && "$SCRIPT_DIR/chezmoi-personal.sh" pull
    PULL=1 TITLE=work "$HOME/bin/gremlins/check-repo-status" "$SCRIPT_DIR"

elif [[ "$ACTION" = "init" ]]; then
    # For 'init', do not pass through any url, 'init' with no args is OK (refreshes `chezmoi.toml`)
    set -x
    [[ -z "$WORK_ONLY" ]] && "$SCRIPT_DIR/chezmoi-personal.sh" init
    chezmoi init

elif [[ -n "$WORK_ONLY" || "$ACTION" == (apply|diff|managed|status|unmanaged|update) ]]; then
    if [[ -z "$WORK_ONLY" ]]; then
        echo "---- personal $ACTION: ----"
        "$SCRIPT_DIR/chezmoi-personal.sh" "$@"
        echo "---- work $ACTION: ----"
    fi
    chezmoi "$@"

else
    echo "Command '$ACTION' not supported for this multi-dotfiles repo setup"
    exit 1

fi
```

## The `check-repo-status` helper

Both wrappers print a per-repo status line via `check-repo-status`, so `cz` ends up showing:

```shell
$ cz
[personal] ✨ Up to date
[work] ✨ Up to date
```

It's a small helper: pass it a **repo path** and it fetches that repo and reports its state
(`✨ Up to date`, `N behind`, `N pending`). The label in brackets is the directory name, or a
`TITLE=` override:

```shell
$ ~/bin/gremlins/check-repo-status                       # no path → uses cwd
fatal: not a git repository (or any of the parent directories): .git
$ ~/bin/gremlins/check-repo-status ~/.local/share/chezmoi
[chezmoi] ✨ Up to date
$ TITLE=personal ~/bin/gremlins/check-repo-status ~/.local/share/pd/personal-dotfiles
[personal] ✨ Up to date
```

It lives in this repo:
[`home/bin/gremlins/executable_check-repo-status`](https://github.com/zsimic/dotfiles/blob/main/home/bin/gremlins/executable_check-repo-status)
(chezmoi deploys it to `~/bin/gremlins/check-repo-status`). Grab it as-is, or drop those lines
and use plain `git -C <repo> fetch` / `git -C <repo> status` if you'd rather keep the wrappers
dependency-free.
