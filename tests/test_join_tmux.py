import os

import runez

JOIN_TMUX = "home/bin/gremlins/executable_join-tmux"


def test_help(cli):
    cli.main = JOIN_TMUX
    cli.run("--help")
    assert cli.succeeded
    assert "usage:" in cli.logged


def test_tmux(cli, monkeypatch):
    cli.main = JOIN_TMUX
    monkeypatch.delenv("TMUX", raising=False)
    monkeypatch.delenv("GHOSTTY_BIN_DIR", raising=False)
    monkeypatch.setenv("ITERM_PROFILE", "foo")
    cli.run("-nv", "test")
    assert cli.succeeded
    assert "Would run: tmux new-session -d -s test-iterm" in cli.logged.stdout
    assert "Would exec: exec tmux attach-session -t test-iterm" in cli.logged.stdout

    monkeypatch.setenv("GHOSTTY_BIN_DIR", "some-path")
    monkeypatch.setenv("TMUX", "some-socket")
    monkeypatch.setenv("TMUX_CONFIG", ".")
    monkeypatch.delenv("PATH", raising=False)
    assert not os.path.exists("test.log")
    runez.write("tmux.test.cfg", "~\ndev", logger=None)
    cli.run("-nv", "--log", "test.log", "test")
    assert cli.succeeded
    assert "Would abort: Already in tmux" in cli.logged.stdout
    assert "Would run: tmux new-session -d -s test-ghostty" in cli.logged.stdout
    assert os.path.exists("test.log")

    monkeypatch.setenv("SSH_TTY", "some-socket")
    monkeypatch.setenv("TERM", "tmux-256color")
    monkeypatch.delenv("TMUX", raising=False)
    cli.run("-v", "test")
    assert cli.failed
    assert "TERM: tmux-256color" in cli.logged.stderr
    assert "Already in tmux" in cli.logged.stderr
