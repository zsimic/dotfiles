# uv-metadata exploration

## Spec

A script that shows the metadata of any python package in JSON format.

Given a pip spec, resolve the **latest version** (in a python-version-agnostic way) and output its metadata.
This answers the question: "what's the latest version of X, and what does its metadata say?" —
in particular `requires_python`, `requires_dist`, `summary`, etc.

```
uv-metadata requests              # latest version, full metadata as JSON
uv-metadata requests -k version   # just the version
uv-metadata 'requests<2'          # latest matching the constraint
uv-metadata -p3.7 setuptools      # "what's the latest for python 3.7?"
```

The optional `-p` flag rephrases the question as "what's the latest version compatible with this python?".
Without it, the script returns the absolute latest version regardless of python.

Local paths and git URLs are out of scope for this script — we already have a solid implementation for those.


## Test cases

These cases should all produce correct results:

| Command | Expected version | Path | Notes |
|---|---|---|---|
| `uv-metadata requests -k version` | 2.33.1 | wheel (streaming) | Pure python wheel |
| `uv-metadata 'requests<2' -k version` | 1.2.3 | sdist | Ancient, no wheels exist |
| `uv-metadata 'grpcio-tools<1.70' -k version` | 1.69.0 | sdist | C extension, no wheels for default python (cp314) |
| `uv-metadata torch -k version` | 2.11.0 | wheel (streaming) | 80MB wheel, no sdist — streaming reads only a few KB |
| `uv-metadata mysqlclient -k version` | 2.2.8 | wheel (streaming) | Windows-only wheels, no linux wheels |
| `uv-metadata setuptools -k version` | 82.0.1 | wheel (streaming) | Latest |
| `uv-metadata -p3.7 setuptools -k version` | 68.0.0 | wheel (streaming) | Latest for python 3.7 |
| `uv-metadata 'pycparser<2.17' -k version` | 2.16 | sdist | Old, no wheels |
| `uv-metadata pytest -k entry_points` | (dict) | wheel (streaming) | Verifies entry_points extraction |
| `uv-metadata pytest -k top_level` | (list) | wheel (streaming) | Verifies top_level extraction |
| `uv-metadata 'non-existent-project22'` | error exit | — | Clear error from uv |


## Findings

### Resolution: `uv pip compile` with pylock.toml

The key discovery is that a single `uv pip compile` call gives us everything we need:

```
echo <spec> | uv -q pip compile \
  --no-deps --no-header --universal \
  --format=pylock.toml --fork-strategy fewest --no-sources -
```

This outputs a pylock.toml with:
- The resolved version
- All available wheels across all platforms (with URLs and sizes)
- The sdist URL (if any)

The flags:
- `--no-deps`: we only care about the package itself
- `--universal`: show wheels for ALL platforms, not just the current one
- `--fork-strategy fewest`: always produces exactly one package entry (avoids multiple entries for different python ranges)
- `--no-sources`: ignore local pyproject.toml sources
- No `--python-version` by default: resolves to the absolute latest version

Adding `--python-version 3.7` (via the `-p` flag) rephrases the question to "latest for this python".

### Metadata extraction: two paths, one parser

Both paths produce a `.dist-info` directory on disk, then `dist_info_to_dict()` handles
all parsing via stdlib `importlib.metadata.PathDistribution` — METADATA, entry_points.txt,
and top_level.txt in one place.

#### Wheels (most packages): streaming via HTTP range requests

Uses `seekablehttpfile` to stream just the `.dist-info` files from a remote wheel
without downloading it. Inspired by `metadata_please`, but inlined since all we need
is `zf.read()` on a few files. Pick any wheel from the resolved list — metadata is
identical across platforms.

```python
from seekablehttpfile import SeekableHttpFile
import zipfile

zf = zipfile.ZipFile(SeekableHttpFile(wheel_url))
# Find the .dist-info dir from the zip central directory
# Extract METADATA, entry_points.txt, top_level.txt into a temp dir
# Then use dist_info_to_dict() to parse — same as local .dist-info
```

How it works:
1. `SeekableHttpFile(url)` wraps a remote URL as a seekable file-like object using HTTP range requests
2. `ZipFile` reads the central directory from the end of the file (a few KB, regardless of wheel size)
3. `zf.read()` fetches each `.dist-info` entry individually (METADATA, entry_points.txt, top_level.txt)
4. Files are written to a temp `.dist-info` dir, then `PathDistribution` parses everything

This means an 80MB torch wheel only transfers a few KB over the wire.

**Why not `pkginfo.Wheel`?**
`pkginfo.Wheel(path)` requires a file path — it calls `os.path.exists()` internally
and creates its own `ZipFile`. It cannot accept a `ZipFile` or file-like object,
which makes the streaming pattern impossible with it.

#### Sdist (rare fallback): download + pkginfo

For packages with no wheels at all (e.g., `pycparser<2.17`, `requests<2`):
download the sdist tarball and use `pkginfo.SDist(path)` to read PKG-INFO.
No build needed — PKG-INFO is at the top of the tarball.

The sdist URL comes directly from the pylock.toml resolution output.

### `dist_info_to_dict`: single metadata parser

All wheel metadata goes through `dist_info_to_dict(path)`, which uses stdlib
`importlib.metadata.PathDistribution`. It handles:
- `.metadata` — the METADATA file (name, version, requires_dist, etc.)
- `.entry_points` — parsed entry_points.txt (console_scripts, etc.)
- `.read_text("top_level.txt")` — top-level package names

This function also works standalone with any local `.dist-info` directory
(e.g., after `uv pip install --no-deps --target`).

### Why `--python-version` is NOT passed by default

Without `--python-version`, `uv pip compile` uses the system python for resolution.
This means fewer wheels may be discovered (e.g., grpcio-tools 1.69.0 has no cp314 wheels),
but those cases fall through to the sdist path which handles them cleanly.

Passing `--python-version 3.12` would discover more wheels (broadest coverage), but:
- Adds a default that needs to be maintained
- The sdist fallback works well for the few cases where it matters
- Keeps the code simpler

### Dependencies

- `uv` — resolution via `uv pip compile`
- `seekablehttpfile` — HTTP range requests for streaming wheel access
- `pkginfo` — reads PKG-INFO from sdist tarballs (fallback path)
- `tomllib` / `tomli` — parses pylock.toml output
