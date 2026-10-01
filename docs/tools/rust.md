# Rust tool management

[manage-rust-tools] keeps a small set of Rust CLIs installed by compiling them with `cargo install`.
Rust CLIs default to the [Brewfile] (native bottles for macOS and Linux, upgraded monthly); only
those whose formula would pull in extra libraries stay here.

[manage-rust-tools]: ../../home/bin/gremlins/executable_manage-rust-tools
[Brewfile]: ../../home/dot_config/homebrew/Brewfile

## Why some tools stay on cargo

Their Homebrew formulae depend on shared libraries that would then be installed system-wide in the
Homebrew prefix:

| Tool | Extra Homebrew dependencies |
| --- | --- |
| atuin | `openssl@4` (Linux only) |
| bat | `libgit2`, `oniguruma` |
| eza | `libgit2` |
| git-delta | `libgit2`, `oniguruma` (+ `zlib-ng-compat` on Linux) |
| ripgrep | `pcre2` |

`libgit2` itself brings in `libssh2`, `openssl@3`, `ca-certificates` and `llhttp`.

Such libraries in the Homebrew prefix used to interfere with otherwise clean builds, for example
compiling CPython or Python wheels, which may pick up Homebrew's headers and libraries instead of
the system ones. That was mostly a problem back when Homebrew lived in `/usr/local`, but keeping the
prefix free of them is still preferred. The `cargo install` builds statically bundle `libgit2` and
`oniguruma`, and ripgrep's PCRE2 support is an optional feature that is off by default, so the
binaries have no such runtime dependencies.

When adding a Rust CLI, check `brew deps <formula>`: if it is empty, add the formula to the
Brewfile instead.

## Apply lifecycle

The [Rust install hook] includes a hash of the manager. Chezmoi therefore runs it on the first apply
and whenever the manager changes.

[Rust install hook]: ../../home/.chezmoiscripts/run_onchange_after_01-install-rust-tools.sh.tmpl

The manager then:

1. Installs a minimal `rustup` without modifying shell startup files, if necessary.
2. Updates rustup and installed Rust toolchains on later runs.
3. Uninstalls packages listed in `obsolete_rust_packages` (tools moved to the Brewfile, or no longer
   used), plus any leftover `cargo-binstall` state.
4. Installs or upgrades the desired packages plus any other packages already recorded by Cargo, with
   `cargo install --locked` against the host target (so binaries link to the local glibc on Linux).

`cargo-binstall` was dropped: its prebuilt-binary lookups often hit GitHub's unauthenticated API rate
limit, and on Apple Silicon it upgraded itself to its x86_64 build, which then ran every compile under
Rosetta (broken on macOS 27, whose `libxcrun` has no x86_64 slice).

Run the manager directly with:

```zsh
~/bin/gremlins/manage-rust-tools
```

## Monthly upgrade

The [monthly hook] renders the current year and month into the script. The first `chezmoi apply` in
a new month therefore runs [monthly-upgrade], which:

[monthly hook]: ../../home/.chezmoiscripts/run_onchange_after_90-monthly-upgrade.sh.tmpl
[monthly-upgrade]: ../../home/bin/gremlins/executable_monthly-upgrade

1. Runs the Rust manager.
2. Updates Homebrew and upgrades formulae plus casks that do not manage their own updates.
3. Cleans Homebrew's old artifacts.
4. Regenerates managed zsh completions.

This is apply-driven, not a background scheduler. It can also be run explicitly:

```zsh
~/bin/gremlins/monthly-upgrade
```

Edit `desired_rust_packages` in the manager to change the automated Rust inventory; keep
[Automated tools](./automated.md) in sync as the readable index.
