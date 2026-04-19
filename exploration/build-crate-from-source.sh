#!/bin/zsh -eu

setopt pipefail

if (( $# != 1 )); then
    print -u2 "usage: $0 <crate-name>"
    exit 1
fi

zmodload zsh/datetime

typeset -r crate_name="$1"
typeset -r temp_dir="$(mktemp -d "${TMPDIR:-/tmp}/build-crate-from-source.XXXXXX")"
typeset -r install_root="$temp_dir/root"
typeset -r target_dir="$temp_dir/target"

cleanup() {
    [[ -d "$temp_dir" ]] || return 0
    rm -rf "$temp_dir"
}

trap cleanup EXIT INT TERM

print "Building $crate_name from source"
print "Temporary install root: $install_root"

typeset -F6 start_time="$EPOCHREALTIME"

# Keep the build isolated so we can measure a clean cargo install without
# touching the real cargo install root.
CARGO_TARGET_DIR="$target_dir" cargo install --root "$install_root" --force --locked -- "$crate_name"

typeset -F6 end_time="$EPOCHREALTIME"
typeset -F3 elapsed_seconds="$(( end_time - start_time ))"

print "Elapsed: ${elapsed_seconds}s"
