import json
import runpy
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "home/bin/gremlins/executable_upgrade-uv-pythons"


@pytest.fixture
def manager():
    return runpy.run_path(str(SCRIPT))


def installation(version, *, arch="aarch64", variant="default", implementation="cpython"):
    suffix = "" if variant == "default" else f"+{variant}"
    return {
        "key": f"{implementation}-{version}{suffix}-macos-{arch}-none",
        "version": version,
        "path": f"/pythons/{version}/bin/python",
        "implementation": implementation,
        "variant": variant,
        "os": "macos",
        "arch": arch,
        "libc": "none",
    }


def fake_uv(manager, monkeypatch, installed, available=(), *, fail_install=False, refresh=None):
    calls = []
    installed_after = list(installed) if isinstance(installed, list) else installed

    def run_uv(*args, capture=False):
        calls.append(args)
        if capture:
            return json.dumps(available if "--only-downloads" in args else installed_after)
        if args[:2] == ("python", "install"):
            if fail_install:
                raise subprocess.CalledProcessError(1, ["uv", *args])
            installed_after.extend(record for record in available if record["key"] in args[2:])
            if refresh is not None:
                installed_after[:] = refresh
        return None

    monkeypatch.setitem(manager["maintain"].__globals__, "run_uv", run_uv)
    return calls


def test_cleanup_preserves_families_and_variants(manager, monkeypatch):
    records = [
        installation("3.14.2"),
        installation("3.14.10"),
        installation("3.14.1", arch="x86_64"),
        installation("3.12.13"),
        installation("3.12.16"),
        installation("3.10.22"),
        installation("3.12.10", implementation="pypy"),
        installation("3.12.15", implementation="pypy"),
        installation("3.14.1", variant="freethreaded"),
        installation("3.14.2", variant="freethreaded"),
        installation("3.14.1", variant="debug"),
    ]
    calls = fake_uv(manager, monkeypatch, records)
    assert manager["main"](["--commit"]) == 0
    assert calls[-1] == ("python", "uninstall", *(records[i]["key"] for i in (3, 0, 8, 6)))
    assert len(calls) == 3


def test_default_preview_includes_upgrades(manager, monkeypatch, capsys):
    old = installation("3.12.10", implementation="pypy")
    new = installation("3.12.15", implementation="pypy")
    calls = fake_uv(manager, monkeypatch, [old], [new, installation("3.15.0")])
    assert manager["main"]([]) == 0
    assert len(calls) == 2
    assert all("list" in call for call in calls)
    assert "--all-platforms" not in calls[1]
    assert "--all-arches" not in calls[1]
    output = capsys.readouterr().out
    assert "dryrun mode by default, use --commit to enact these changes" in output
    assert "Would install: pypy-3.12.15" in output
    assert "Would uninstall: pypy-3.12.10" in output
    assert "3.15.0" not in output


@pytest.mark.parametrize("implementation", ["cpython", "pypy"])
def test_binary_numeric_ordering(manager, implementation):
    binary_type = manager["PythonBinary"]
    older = binary_type.from_record(installation("3.12.9", implementation=implementation))
    newer = binary_type.from_record(installation("3.12.15", implementation=implementation))
    assert older.major == 3
    assert older.minor == 12
    assert older.patch == 9
    assert older.family == newer.family
    assert sorted([newer, older]) == [older, newer]
    assert max({older, newer}) == newer
    prefix = "" if implementation == "cpython" else "pypy-"
    assert newer.short_name == f"{prefix}3.12.15"
    assert newer.minor_name == f"{prefix}3.12"


@pytest.mark.parametrize("implementation", ["cpython", "pypy", "graalpy", "pyodide"])
def test_upgrade_then_refresh_then_cleanup(manager, monkeypatch, implementation):
    old = installation("3.12.10", implementation=implementation)
    new = installation("3.12.15", implementation=implementation)
    calls = fake_uv(manager, monkeypatch, [old], [new])
    assert manager["main"](["--commit"]) == 0
    assert calls[2] == ("python", "install", new["key"])
    assert "--only-installed" in calls[3]
    assert calls[4] == ("python", "uninstall", old["key"])


def test_failed_install_prevents_cleanup(manager, monkeypatch, capsys):
    calls = fake_uv(manager, monkeypatch, [installation("3.14.2")], [installation("3.14.10")], fail_install=True)
    assert manager["main"](["--commit"]) == 1
    assert len(calls) == 3
    assert "upgrade-uv-pythons:" in capsys.readouterr().err


def test_missing_new_installation_prevents_cleanup(manager, monkeypatch):
    calls = fake_uv(manager, monkeypatch, [installation("3.14.2")], [installation("3.14.10")], refresh=[])
    assert manager["main"](["--commit"]) == 1
    assert not any("uninstall" in call for call in calls)


def test_no_downgrades_or_prereleases(manager, monkeypatch, capsys):
    records = [installation("3.14.10")]
    calls = fake_uv(manager, monkeypatch, records, [installation("3.14.2"), installation("3.14.11rc1"), installation("3.16.0a1")])
    assert manager["main"](["--commit"]) == 0
    assert len(calls) == 2
    assert capsys.readouterr().out == "up-to-date: 3.14\n"


def test_prerelease_ordering(manager):
    versions = ["3.16.0a1", "3.16.0a2", "3.16.0a10", "3.16.0b1", "3.16.0rc1", "3.16.0rc2", "3.16.0", "3.16.1"]
    binaries = [manager["PythonBinary"].from_record(installation(version)) for version in versions]
    assert all(older < newer for older, newer in zip(binaries, binaries[1:]))
    assert binaries[0].minor_name == "3.16.0a1"
    assert binaries[0].short_name == "3.16.0a1"


@pytest.mark.parametrize(
    ("older", "newer"), [("3.16.0a1", "3.16.0a2"), ("3.16.0a10", "3.16.0b1"), ("3.16.0b2", "3.16.0rc1"), ("3.16.0rc2", "3.16.0")]
)
def test_upgrade_prereleases(manager, monkeypatch, capsys, older, newer):
    old, new = installation(older), installation(newer)
    calls = fake_uv(manager, monkeypatch, [old], [new])
    assert manager["main"](["--commit"]) == 0
    assert calls[2] == ("python", "install", new["key"])
    assert calls[-1] == ("python", "uninstall", old["key"])
    assert f"Installing: {newer}" in capsys.readouterr().out


def test_current_alpha_is_visible(manager, monkeypatch, capsys):
    fake_uv(manager, monkeypatch, [installation("3.16.0a1")], [installation("3.16.0a1")])
    assert manager["main"]([]) == 0
    assert capsys.readouterr().out.endswith("up-to-date: 3.16.0a1\n")


def test_unknown_version_is_ignored(manager):
    assert manager["parse_inventory"]([installation("3.16.0.dev1")]) == set()


@pytest.mark.parametrize("records", [[], [installation("3.10.22")]])
def test_no_cleanup_needed(manager, monkeypatch, records):
    calls = fake_uv(manager, monkeypatch, records)
    assert manager["main"](["--commit"]) == 0
    assert len(calls) == 2


@pytest.mark.parametrize(
    "records",
    [
        {},
        [None],
        [{}],
        [dict(installation("3.14.2"), version="3.14.10")],
        [dict(installation("3.14.2"), arch=None)],
        [dict(installation("3.14.2"), path=None)],
        [dict(installation("3.14.2"), version=None)],
    ],
)
def test_bad_inventory_prevents_mutations(manager, monkeypatch, records):
    calls = fake_uv(manager, monkeypatch, records)
    assert manager["main"](["--commit"]) == 1
    assert len(calls) == 1


def test_entrypoint_and_uv_invocation(monkeypatch):
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        assert kwargs["check"] is True
        assert kwargs["stdout"] == subprocess.PIPE
        return subprocess.CompletedProcess(command, 0, stdout="[]")

    monkeypatch.setattr(subprocess, "run", run)
    monkeypatch.setattr(sys, "argv", [str(SCRIPT)])
    with pytest.raises(SystemExit) as error:
        runpy.run_path(str(SCRIPT), run_name="__main__")
    assert error.value.code == 0
    assert len(calls) == 2
    assert calls[0][:2] == ["uv", "--no-config"]


def test_missing_uv(manager, monkeypatch):
    def missing(*_args, **_kwargs):
        raise FileNotFoundError("uv")

    monkeypatch.setattr(subprocess, "run", missing)
    assert manager["main"]([]) == 1
