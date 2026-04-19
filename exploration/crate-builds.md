# Rust crate source-build timings

Measured on 2026-04-19 by running `./exploration/build-crate-from-source.sh <crate>` for each crate managed by `home/bin/gremlins/executable_manage-rust-tools`.

Notes:
- Each run used a temporary `cargo install --root` and a temporary `CARGO_TARGET_DIR`.
- The helper cleaned up its temporary directory after each run.
- Timings are wall-clock `Elapsed` values reported by the helper.
- These are not fully cold builds: Cargo still reused the normal registry/index/download cache between runs.
- `uv` is included because the current user is `zoran`, matching the conditional in `executable_manage-rust-tools`.

## Results

| Crate | Version | Elapsed | Notes |
| --- | --- | ---: | --- |
| `uv` | `0.11.7` | 128.578s | Clear outlier; multi-minute class. |
| `bat` | `0.26.1` | 35.543s | Heavier than the rest of the non-`uv` set. |
| `dua-cli` | `2.34.0` | 26.804s | Mid-weight compile. |
| `eza` | `0.23.4` | 24.398s | Mid-weight compile. |
| `git-delta` | `0.19.2` | 23.904s | Built successfully with `--locked`; Cargo warned about yanked lockfile deps. |
| `fd-find` | `10.4.2` | 21.205s | Fairly quick source build. |
| `cargo-update` | `20.0.0` | 14.544s | Fast enough that source builds seem tolerable. |
| `tokei` | `14.0.0` | 13.839s | Built successfully with `--locked`; Cargo warned about a yanked lockfile dep. |
| `zoxide` | `0.9.9` | 11.150s | Quick source build. |
| `ripgrep` | `15.1.0` | 7.520s | Very quick source build. |
| `tre-command` | `0.4.0` | 6.182s | Fastest in the set. |

## Sorted takeaways

If the goal is "avoid the painful source builds during monthly upgrade", this run suggests:

- `uv` is the strongest candidate to keep off the source-build path.
- `bat` is the next most noticeable one, but still under 40 seconds.
- Everything else landed roughly between 6 and 27 seconds on this machine.
