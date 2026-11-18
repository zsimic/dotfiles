# Python maintenance

## uv-managed Pythons

[upgrade-uv-pythons] moves every Python uv already has to its latest known patch, then uninstalls the
superseded ones. It previews by default; `--commit` acts. On personal machines the [weekly hook] runs it
with `--commit` on the first apply of each seven-day period (apply-driven, not scheduled) and whenever the
helper changes.

Decisions behind it:

- It never adds a minor or implementation, and never downgrades: install or remove those by hand
  (`uv python install 3.15`, `uv python install pypy@3.12`, `uv python uninstall 3.10`).
- It uses `uv python install` with exact keys rather than `uv python upgrade`, which only handles
  CPython; PyPy, GraalPy and Pyodide get the same treatment.
- Installing a prerelease opts that minor into prereleases until its final release; stable installs
  never adopt them.
- It reads uv's bundled catalog offline with `--no-config`, so the working directory and uv config files
  don't affect it (environment overrides like `UV_PYTHON_INSTALL_DIR` still do). Upgrading uv itself is
  out of scope.
- Known gaps: a new PyPy or GraalPy build with the same Python version isn't detected. Venvs pinned to
  an exact patch (and non-CPython venvs) may need recreating after cleanup, an accepted tradeoff on
  personal machines; uv CPython venvs normally follow the minor-version symlink.

[upgrade-uv-pythons]: ../../home/bin/gremlins/executable_upgrade-uv-pythons
[weekly hook]: ../../home/.chezmoiscripts/personal/run_onchange_after_95-weekly-upgrade-uv-pythons.sh.tmpl

## Pickley interpreter selection

On personal machines, [pickley's configuration] makes it look for Pythons in `~/.local/bin`, where uv
maintains the versioned links. Choose the default with relative links; pickley follows `python3 ->
python3.15` on its own, so no `preferred_pythons` setting is needed:

```sh
ln -sf python3.15 ~/.local/bin/python3
ln -sf python3.15 ~/.local/bin/python
```

Existing CLI environments keep their Python until reinstalled; `pickley diagnostics` shows the
selection and `pickley -n install -f mgit` previews a forced reinstall.

[pickley's configuration]: ../../home/dot_local/bin/dot_pk/config.json
