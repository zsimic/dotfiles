# Python maintenance

[upgrade-uv-pythons] upgrades Python implementations already installed by uv, then uninstalls superseded
stable patches. It uses uv's normal storage and CPython minor-version symlinks.

[upgrade-uv-pythons]: ../../home/bin/gremlins/executable_upgrade-uv-pythons

```sh
~/bin/gremlins/upgrade-uv-pythons
~/bin/gremlins/upgrade-uv-pythons --commit
```

The default is a read-only preview: `dryrun mode by default, use --commit to enact these changes`.
It shows exact installations to add, retain, and remove using the installed uv's bundled download
catalog. Only `--commit` installs or uninstalls anything.

Output groups minor versions and pending changes into compact lines, for example:

```text
dryrun mode by default, use --commit to enact these changes
up-to-date: 3.14, 3.13, 3.12, 3.10, pypy-3.12
Would uninstall: 3.12.13, 3.13.13, 3.14.2
```

Pending installs and removals include the patch version. Non-CPython names carry their implementation
prefix. Free-threaded builds use the compact `t` suffix (such as `3.15t`); other non-default builds
keep their variant suffix. uv commands still use the full installation keys.

Catalog downloads are limited to uv's current platform and architecture. `--offline` prevents network
access while listing, and `--no-cache` avoids persistent cache writes during previews. `--no-config`
ignores project and user uv configuration files so the working directory does not affect maintenance.
Environment overrides such as `UV_PYTHON_INSTALL_DIR` still apply; the flag does not force default storage.

## Pickley interpreter selection

On personal machines, chezmoi manages [pickley's configuration] at `~/.local/bin/.pk/config.json`.
It searches `~/.local/bin` for Python installations. Select the preferred Python with relative links:

```sh
ln -sf python3.15 ~/.local/bin/python3
ln -sf python3.15 ~/.local/bin/python
```

[pickley's configuration]: ../../home/dot_local/bin/dot_pk/config.json

Pickley follows `python3 -> pythonM.m` automatically, so no `preferred_pythons` setting is needed.
uv maintains the versioned links; the relative links above select the default.
Existing CLI environments are unchanged until reinstalled.

Inspect the selection and preview a forced reinstall with:

```sh
pickley diagnostics
pickley -n install -f mgit
```

## Policy

- Install and remove implementation/minor families manually, for example `uv python install 3.15`,
  `uv python install pypy@3.12`, or `uv python uninstall 3.10`. Automatically downloaded Pythons are
  also part of uv's installed inventory.
- Select the latest stable Python patch known to the installed uv for each installed implementation,
  minor, build variant, OS, architecture, and libc. Never introduce another minor or implementation,
  or downgrade a newer installed patch. Leave prerelease installations alone.
- Use `uv python install` with exact installation keys. Unlike `uv python upgrade`, this also handles
  PyPy, GraalPy, and Pyodide. uv maintains CPython's minor links when installing newer patches.
- After all installs succeed, inventory again and verify the new installations are present. Retain
  the newest installed stable patch in each family and uninstall older patches using exact keys.
- Stop on errors before cleanup. Upgrading uv itself is outside this helper's scope.

The version tracked here is the Python language version exposed by uv's catalog. A new PyPy or
GraalPy build with the same Python version/key is not detected or reinstalled by this helper.

New uv CPython virtual environments normally use a stable minor-version symlink and follow patch
upgrades. Old environments or environments tied to an exact patch may need recreation after cleanup;
this is an accepted tradeoff on personal machines. uv does not provide transparent patch upgrades
for alternative implementations, so their environments may also need recreation.

The [weekly personal hook] calls the helper with `--commit` on the first apply in each seven-day
Unix-time period. Changes to the helper also trigger a run. This is apply-driven, without a background
scheduler; the first apply after adding the hook runs it immediately.

[weekly personal hook]: ../../home/.chezmoiscripts/personal/run_onchange_after_95-weekly-upgrade-uv-pythons.sh.tmpl

See uv's [Python upgrade documentation] for its implementation limitations, minor symlinks, and
virtual environment behavior.

[Python upgrade documentation]: https://docs.astral.sh/uv/concepts/python-versions/#upgrading-python-versions
