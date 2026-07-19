# Rust tool management

[manage-rust-tools] keeps a curated set of Rust CLIs installed without requiring a separate package
manager or compiling every tool on every machine.

[manage-rust-tools]: ../../home/bin/gremlins/executable_manage-rust-tools

## Apply lifecycle

The [Rust install hook] includes a hash of the manager. Chezmoi therefore runs it on the first apply
and whenever the manager changes.

[Rust install hook]: ../../home/.chezmoiscripts/run_onchange_after_01-install-rust-tools.sh.tmpl

The manager then:

1. Installs a minimal `rustup` without modifying shell startup files, if necessary.
2. Updates rustup and installed Rust toolchains on later runs.
3. Installs `cargo-binstall`, if necessary.
4. Removes explicitly obsolete Cargo packages.
5. Installs or upgrades the desired packages plus any other packages already recorded by Cargo.

## Binary-first installation

`cargo-binstall` first uses crate metadata to locate a release binary. On Linux x86-64 and ARM64,
the lookup requests a musl target so a downloaded binary does not silently require a newer glibc
than the host provides.

If no suitable binary is available, the manager compiles against the host target. Packages marked
`no-compile` are skipped with a warning instead of triggering that fallback.

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
2. Updates and upgrades Homebrew packages and casks, including greedy cask upgrades.
3. Cleans Homebrew's old artifacts.
4. Regenerates managed zsh completions.

This is apply-driven, not a background scheduler. It can also be run explicitly:

```zsh
~/bin/gremlins/monthly-upgrade
```

Edit `desired_rust_packages` in the manager to change the automated Rust inventory; keep
[Automated tools](./automated.md) in sync as the readable index.
