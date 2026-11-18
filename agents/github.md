# github.com

Remotes use https, so a box without an ssh key (e.g. a headless server) can still clone and pull, the
dotfiles repo included. `pushInsteadOf` in `~/.config/git/config-personal` sends pushes over ssh, so
they fail cleanly where there is no key. Keep `https://github.com/…` remotes as is (no switching to
ssh, no `insteadOf` rewrites); if a push fails (no key, sandbox), ask the user to run it.
