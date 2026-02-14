import os
import sys
from pathlib import Path

import executable_shrinky as shrinky
import runez


def test_clean_path(cli):
    runez.touch("foo/bar/readme.txt")
    cli.run("clean_path -pfoo:baz:foo/bar:baz2:/foo/bar/baz", main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "foo:foo/bar\n"


def test_colors():
    x = shrinky.ColorSet.color_set_by_name("zsh")
    assert str(x) == "zsh-ps1"
    assert str(x.bold) == "%Bbold%b"

    x = shrinky.ColorSet.color_set_by_name("tty")
    assert str(x) == "tty-colors"


def test_get_path():
    cwd = Path(".").resolve()
    assert shrinky.get_path(None) == cwd
    assert shrinky.get_path("") == cwd
    assert shrinky.get_path(".") == Path(".")
    assert shrinky.get_path('"."') == Path(".")
    assert shrinky.get_path(Path(".")) == Path(".")

    user_dir = Path(os.path.expanduser("~"))
    assert shrinky.get_path("~") == user_dir
    assert shrinky.get_path('"~"') == user_dir


def test_help(cli):
    cli.run("--help", main=shrinky.main)
    assert cli.succeeded
    assert "Usage:" in cli.logged.stderr

    cli.run("tmux_status --help", main=shrinky.main)
    assert cli.succeeded
    assert "Example:\n  set -g status-right" in cli.logged.stderr


def test_invalid(cli, monkeypatch):
    assert shrinky.run_program("~does-not-exist") is None

    cli.run("", main=shrinky.main)
    assert cli.failed
    assert "No command provided" in cli.logged.stderr

    cli.run("foo", main=shrinky.main)
    assert cli.failed
    assert cli.logged.stderr.contents() == "Unknown command 'foo'\n"
    assert not cli.logged.stdout

    cli.run("ps1 foo", main=shrinky.main)
    assert cli.failed
    assert cli.logged.stderr.contents() == "Unrecognized argument 'foo'\n"

    cli.run("ps1", main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == ": \n"

    cli.run("ps1 -cfoo", main=shrinky.main)
    assert cli.failed
    assert cli.logged.stderr.contents() == "No color set for 'foo'\n"

    cli.run("ps1 -z5", main=shrinky.main)
    assert cli.failed
    assert cli.logged.stderr.contents() == "Unknown flag 'z'\n"

    # Simple message on stderr on crash
    monkeypatch.setattr(shrinky, "folder_parts", lambda *_: None)
    cli.run("-v ps1 -czsh -pfoo/bar", main=shrinky.main)
    assert cli.failed
    assert "'ps1()' crashed: cannot unpack non-iterable NoneType object\n" in cli.logged.stderr
    assert "in cmd_ps1" in cli.logged.stderr


def test_ps1(cli):
    cli.run("ps1 -czsh -uroot -x0 -p/tmp/foo/bar/baz -v", main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "❕ %F{yellow}%{\x1b[2m%}/t/f/bar/%{\x1b[22m%}baz%f%F{green} #%f \n"

    # User shown when not matching stated owner
    cli.run("ps1 -czsh -uuser1 -ouser2,user3 -x1", main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "%F{blue}user1%f@%F{red}:%f \n"

    # This test's own venv
    venv_path = os.path.dirname(os.path.dirname(sys.executable))
    py_version = ".".join(str(x) for x in sys.version_info[:2])
    cli.run("ps1", "-czsh", "-x1", "-v%s" % venv_path, main=shrinky.main)
    assert cli.succeeded
    output = cli.logged.stdout.contents()
    assert py_version in output

    # A fictional venv
    cli.run("ps1", "-czsh", "-vfoo/bar/.venv", main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "(%F{cyan}bar%f %F{blue}None%f) %F{green}:%f \n"

    # Minimal args
    cli.run("ps1 -cbash", main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "\\[\x1b[32m\\]:\\[\x1b[39m\\] \n"


def test_ps1_deep(cli, monkeypatch):
    sample = "sample/some/very/deep/folder/with/way/too/many/characters/tests"
    runez.touch("%s/.git" % sample)
    full_path = os.path.abspath("%s/foo/bar/baz/even/more/tests" % sample)
    venv = "%s/.venv" % full_path
    runez.write("%s/bin/activate" % venv, '\nPS1="(some-very-long-venv-prompt) ${PS1:-}"')
    cli.run('ps1 -cplain -p"%s" -v"%s/.venv"' % (full_path, full_path), main=shrinky.main)
    assert cli.succeeded
    expected = "(𓈓me-very-long-venv-prompt None) /𓈓/f/b/b/e/more/tests: \n"
    assert cli.logged.stdout.contents() == expected

    # Simulate docker
    monkeypatch.setattr(shrinky.Ps1Renderer, "dockerenv", ".")
    cli.run("ps1 -czsh", main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "🐳 %F{green}:%f \n"

    # Simulate ssh
    monkeypatch.setenv("SSH_TTY", "foo")
    cli.run("ps1 -czsh", main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "%F{cyan} %f%F{green}:%f \n"

    # Simulate coder
    monkeypatch.setenv("CODER", "foo")
    cli.run("ps1 -czsh", main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "%F{cyan} %f%F{green}:%f \n"


def test_tmux(cli, monkeypatch):
    monkeypatch.setattr(shrinky.Logger, "log_location", "test.log")
    cli.run("-v tmux_short -p%s" % os.environ.get("HOME"), main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "~\n"

    cli.run("tmux_short -p~/dev/foo/bar", main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "bar\n"

    # No git folder, no branch shown in tmux status
    cli.run("tmux_status", main=shrinky.main)
    assert cli.succeeded
    assert "fg=yellow" not in cli.logged.stdout.contents()

    # Simulate git detached head
    runez.write(".git/HEAD", "g123", logger=None)
    cli.run("tmux_status", main=shrinky.main)
    assert cli.succeeded
    assert "]g123#[default]" in cli.logged.stdout.contents()

    # Simulate invalid .git folder
    runez.delete(".git/HEAD", logger=None)
    runez.touch(".git/HEAD/foo", logger=None)
    cli.run("tmux_status", main=shrinky.main)
    assert cli.succeeded
    logged = cli.logged.stdout.contents().strip()
    assert "|" not in logged


def test_tmux_here(cli):
    # Exercise real case (this repo)
    project_path = runez.DEV.project_path("bin")
    cli.run("tmux_short -p%s" % project_path, main=shrinky.main)
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "chezmoi/bin\n"

    cli.run("tmux_status -p%s" % project_path, main=shrinky.main)
    assert cli.succeeded
    logged = cli.logged.stdout.contents().strip()
    assert "┆" in logged
    assert "#[default]" in logged


def test_uptime():
    x = shrinky.rendered_uptime("up")
    assert "]-uptime?-#[default]" in x

    x = shrinky.rendered_uptime("14:12 up 4 days, 7:06, 2 users, load averages: 0.23 0.19 0.20")
    assert "]4d 7h#[default]" in x

    x = shrinky.rendered_uptime("4:12pm  up 23 days,  2:03, 3 sessions , load average: 0.00, 0.00, 0.00")
    assert "]23d 2h#[default]" in x

    x = shrinky.rendered_uptime("4:13pm  up  7:00, 1 session , load average: 0.00, 0.00, 0.00")
    assert "]7h 0m#[default]" in x
