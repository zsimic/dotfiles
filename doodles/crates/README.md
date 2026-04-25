# Rust crate source-build timings

Measured on Apr 19 2026 by running `./doodles/crates/build-crate-from-source.sh <crate>`
for the Rust crate candidates in `home/bin/gremlins/executable_manage-rust-tools`.
`xh` was added with the same helper on Apr 24 2026. `du-dust`, `hyperfine`,
and `tailspin` were added with the same helper on Apr 25 2026.

Notes:
- Each run used a temporary `cargo install --root` and a temporary `CARGO_TARGET_DIR`.
- The helper cleaned up its temporary directory after each run.
- Timings are wall-clock `Elapsed` values reported by the helper.
- These are not fully cold builds: Cargo still reused the normal registry/index/download cache between runs.
- `uv` remains listed as a `no-compile` reference crate, though it is not bootstrapped by default.
- `du-dust` is the Cargo package for the `dust` executable; `cargo install dust` resolves to a library crate with no binaries.
- `Binary` shows where `crate-meta-data` resolved: `` for `aarch64-apple-darwin`, `🐧` for `x86_64-unknown-linux-gnu`, `-` for neither.
- Availability was refreshed with `./doodles/crates/check-crate-metadata-support.sh`; this rerun did not hit rate limiting.

## Results

| Crate | Binary | Elapsed | Notes |
| --- | --- | ---: | --- |
| `uv` | `🐧` | 129s | Clear outlier; multi-minute class. |
| `atuin` | `🐧` | 65s | Heavy source build, but metadata binaries resolved on both targets. |
| `bat` | `🐧` | 36s | Heavier than the rest of the non-`uv` set. |
| `dua-cli` | `-` | 27s | Mid-weight compile. |
| `eza` | `🐧` | 24s | Mid-weight compile. |
| `git-delta` | `-` | 24s | Built successfully with `--locked`; Cargo warned about yanked lockfile deps. Metadata resolution looked broken on both targets. |
| `tailspin` | `` | 23s | Built successfully with `--locked`; Cargo warned about a yanked lockfile dep. Executable is `tspin`. |
| `fd-find` | `🐧` | 21s | Fairly quick source build. |
| `xh` | `` | 21s | Fairly quick source build; metadata binary resolved for macOS only. |
| `du-dust` | `🐧` | 20s | Fairly quick source build; installs executable `dust`. Metadata binary resolved for Linux only. |
| `tokei` | `-` | 14s | Built successfully with `--locked`; Cargo warned about a yanked lockfile dep. |
| `hyperfine` | `🐧` | 14s | Quick source build; metadata binaries resolved on both targets. |
| `zoxide` | `` | 11s | Quick source build. |
| `ripgrep` | `` | 7.5s | Very quick source build. |
| `tre-command` | `` | 6.2s | Fastest in the set. |

## Sorted takeaways

If the goal is "avoid the painful source builds during monthly upgrade", this run suggests:

- `uv` is the strongest candidate to keep off the source-build path.
- `atuin` is also fairly heavy from source, though still much lighter than `uv`.
- `bat` is the next most noticeable one, but still under 40 seconds.
- Everything else landed roughly between 6 and 27 seconds on this machine, with `tailspin`, `xh`, `fd-find`, and `du-dust` in the same broad band.
