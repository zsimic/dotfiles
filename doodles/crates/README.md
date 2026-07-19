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
- `du-dust` is the Cargo package for the `dust` executable; `cargo install dust` resolves to a
  library crate with no binaries.
- `Prebuilt` shows where `crate-meta-data` resolved: `` for `aarch64-apple-darwin`, `🐧` for
  `x86_64-unknown-linux-musl`, `-` for neither.
- Linux checks use the musl target because `x86_64-unknown-linux-gnu` does not encode a glibc version floor.
- The musl target is only for prebuilt-binary lookup; source-build fallback uses the host target.
- Times and sizes are indicative source-build time and installed binary size.
- Availability was refreshed with `./doodles/crates/check-crate-metadata-support.sh`; this rerun
  did not hit rate limiting.

## Results

| Crate | Prebuilt | Notes |
| --- | ---: | :--- |
| uv | 🐧 129s 48M | Clear outlier; multi-minute class. |
| atuin | 🐧 65s 25M | Heavy source build, but metadata binaries resolved on both targets. |
| bat | 🐧 36s 5.5M | Heavier than the rest of the non-`uv` set. |
| dua-cli | - 27s 2.2M | Mid-weight compile. |
| eza | 🐧 24s 1.7M | Mid-weight compile. |
| git-delta | - 24s 5.5M | `--locked`; yanked deps; metadata broken on both targets. |
| tailspin | 🐧 23s 2.6M | `--locked`; yanked dep; executable is `tspin`. |
| fd-find | 🐧 21s 2.8M | Fairly quick source build. |
| xh | 🐧 21s 7.4M | Fairly quick source build; metadata binary resolved on both targets. |
| du-dust | 🐧 20s 2.2M | Quick; executable `dust`; Linux metadata binary. |
| tokei | - 14s 3.0M | Built successfully with `--locked`; Cargo warned about a yanked lockfile dep. |
| hyperfine | 🐧 14s 1.1M | Quick source build; metadata binaries resolved on both targets. |
| zoxide | 🐧 11s 916K | Quick source build. |
| ripgrep | 🐧 7.5s 3.9M | Very quick source build. |
| tre-command | 🐧 6.2s 1.5M | Fastest in the set. |

## Sorted takeaways

If the goal is "avoid the painful source builds during monthly upgrade", this run suggests:

- `uv` is the strongest candidate to keep off the source-build path.
- `atuin` is also fairly heavy from source, though still much lighter than `uv`.
- `bat` is the next most noticeable one, but still under 40 seconds.
- Everything else landed roughly between 6 and 27 seconds on this machine, with `tailspin`, `xh`,
  `fd-find`, and `du-dust` in the same broad band.
