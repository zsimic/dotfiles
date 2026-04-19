#!/bin/zsh -eu

setopt pipefail

typeset -gr script_path="${0:A}"
typeset -gr script_dir="${script_path:h}"
typeset -gr repo_root="${script_dir:h}"
typeset -gr manage_rust_tools="$repo_root/home/bin/gremlins/executable_manage-rust-tools"

usage() {
    cat <<EOF
usage: $script_path [--target <triple> ...] [crate...]

Check whether crates resolve with:
  cargo binstall --dry-run --force --no-confirm --strategies crate-meta-data

If no crates are given, the default crate list is extracted from:
  $manage_rust_tools

If no targets are given, the defaults are:
  aarch64-apple-darwin
  x86_64-unknown-linux-gnu
EOF
}

default_crates() {
    awk '
        /^typeset -ga desired_rust_packages=\(/ { in_block = 1; next }
        in_block && /^[[:space:]]*\)/ { exit }
        in_block {
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", $0)
            if ($0 != "") {
                print $0
            }
        }
    ' "$manage_rust_tools"

    if [[ "$USER" == "zoran" ]] &&
        grep -q '^\[\[ "\$USER" == "zoran" \]\] && desired_rust_packages+=(uv)$' "$manage_rust_tools"; then
        print uv
    fi
}

check_crate() {
    local target="$1"
    local crate_name="$2"
    local output
    local rc=0
    local crate_status
    local detail

    output="$(
        cargo binstall \
            --dry-run \
            --force \
            --no-confirm \
            --strategies crate-meta-data \
            --targets "$target" \
            -- "$crate_name" 2>&1
    )" ||
        rc=$?

    if [[ "$output" == *"403 Forbidden"* ]] ||
        [[ "$output" == *"rate limit"* ]] ||
        [[ "$output" == *"will wait for 120s and retry"* ]]; then
        crate_status="rate-limited"
        detail="GitHub API rate limit hit while resolving metadata"
    elif (( rc == 0 )); then
        crate_status="supported"
        if [[ "$output" == *"has been downloaded from github.com"* ]]; then
            detail="resolved via github.com"
        else
            detail="resolved"
        fi
    elif [[ "$output" == *"failed to find or install binaries"* ]] ||
        [[ "$output" == *"bin file "*' not found'* ]]; then
        crate_status="broken-metadata"
        detail="release found, but expected binary layout did not match"
    elif [[ "$output" == *"Fallback to cargo-install is disabled"* ]]; then
        crate_status="no-metadata-binary"
        detail="no crate-meta-data binary resolved"
    else
        crate_status="error"
        detail="$(print -r -- "$output" | tail -n 1)"
    fi

    printf '%-15s %-20s %s\n' "$crate_name" "$crate_status" "$detail"

    if (( rc != 0 )); then
        print -r -- "$output" > "$tmp_dir/$target-$crate_name.log"
    fi

    [[ "$crate_status" == "error" ]]
}

command -v cargo > /dev/null

typeset -a crates
typeset -a requested_targets
typeset -a errors
typeset -a rate_limited
typeset -gr tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/check-crate-metadata-support.XXXXXX")"
typeset -gra default_targets=(
    aarch64-apple-darwin
    x86_64-unknown-linux-gnu
)

cleanup() {
    [[ -d "$tmp_dir" ]] || return 0
    rm -rf "$tmp_dir"
}

trap cleanup EXIT INT TERM

while (( $# > 0 )); do
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;
        -t|--target)
            shift
            if (( $# == 0 )); then
                print -u2 "missing value for --target"
                exit 1
            fi
            requested_targets+=("$1")
            ;;
        --target=*)
            requested_targets+=("${1#*=}")
            ;;
        --)
            shift
            crates+=("$@")
            break
            ;;
        -*)
            print -u2 "unknown option: $1"
            usage
            exit 1
            ;;
        *)
            crates+=("$1")
            ;;
    esac

    shift
done

if (( ${#requested_targets[@]} == 0 )); then
    requested_targets=("${default_targets[@]}")
fi

if (( ${#crates[@]} == 0 )); then
    crates=($(default_crates))
fi

typeset -U requested_targets
typeset -U crates

for target in "${requested_targets[@]}"; do
    print "Target: $target"
    print "Strategy: crate-meta-data"
    print
    printf '%-15s %-20s %s\n' "crate" "status" "detail"
    printf '%-15s %-20s %s\n' "-----" "------" "------"

    for crate_name in "${crates[@]}"; do
        if check_crate "$target" "$crate_name"; then
            errors+=("$target/$crate_name")
        fi

        if [[ -f "$tmp_dir/$target-$crate_name.log" ]] &&
            grep -qiE '403 Forbidden|rate limit|will wait for 120s and retry' "$tmp_dir/$target-$crate_name.log"; then
            rate_limited+=("$target/$crate_name")
        fi
    done

    print
done

if (( ${#rate_limited[@]} != 0 )); then
    print -u2 "Warning: rate limiting was encountered for: ${rate_limited[*]}"
    print -u2 "Those results may be incomplete."
fi

if (( ${#errors[@]} != 0 )); then
    print -u2 "Unexpected errors were captured for: ${errors[*]}"
    print -u2 "Logs were written under: $tmp_dir"
    trap - EXIT INT TERM
    exit 1
fi
