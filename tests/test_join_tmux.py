import importlib.machinery
import importlib.util
import os
from pathlib import Path

import runez

PROJECT_DIR = Path(__file__).parent.parent
JOIN_TMUX = str(PROJECT_DIR / "home/bin/executable_join-tmux")


def load_join_tmux_module():
    loader = importlib.machinery.SourceFileLoader("join_tmux_module", JOIN_TMUX)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_help(cli):
    m = load_join_tmux_module()
    assert m

    cli.main = JOIN_TMUX
    cli.run("--help")
    assert cli.succeeded
    assert "usage:" in cli.logged


def test_tmux(cli, monkeypatch):
    cli.main = JOIN_TMUX
    monkeypatch.delenv("TMUX", raising=False)
    monkeypatch.delenv("GHOSTTY_BIN_DIR", raising=False)
    monkeypatch.setenv("ITERM_PROFILE", "foo")
    monkeypatch.setenv("JOIN_TMUX_LOG", "test.log")
    assert not os.path.exists("test.log")
    cli.run("-nv", "test")
    assert cli.succeeded
    assert "Would run: tmux new-session -d -s test-iterm" in cli.logged.stdout
    assert "Would exec: exec tmux attach-session -t test-iterm" in cli.logged.stdout
    assert not os.path.exists("test.log")  # Not effectively logged to file in dryrun mode

    monkeypatch.setenv("GHOSTTY_BIN_DIR", "some-path")
    monkeypatch.setenv("TMUX", "some-socket")
    monkeypatch.setenv("TMUX_CONFIG", ".")
    monkeypatch.delenv("PATH", raising=False)
    runez.write("tmux.test.cfg", "~\ndev", logger=None)
    cli.run("-nv", "test")
    assert cli.succeeded
    assert "Would abort: Already in tmux" in cli.logged.stdout
    assert "Would run: tmux new-session -d -s test-ghostty" in cli.logged.stdout

    monkeypatch.setenv("SSH_TTY", "some-socket")
    monkeypatch.setenv("TERM", "tmux-256color")
    monkeypatch.delenv("TMUX", raising=False)
    assert not os.path.exists("test.log")
    cli.run("-v", "test")
    assert cli.failed
    assert "Already in tmux" in cli.logged.stderr
    assert os.path.exists("test.log")
