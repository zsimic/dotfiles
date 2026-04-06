import os
import sys

import runez

SHRINKY = "home/bin/gremlins/executable_shrinky"


def test_clean_path(cli):
    cli.main = SHRINKY
    runez.touch("foo/bar/readme.txt")
    cli.run("clean_path -pfoo:baz:foo/bar:baz2:/foo/bar/baz")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "foo:foo/bar"


def test_help(cli):
    cli.main = SHRINKY
    cli.run("--help")
    assert cli.succeeded
    assert "Usage:" in cli.logged.stderr

    cli.run("tmux_status --help")
    assert cli.succeeded
    assert "Example:\n  set -g status-right" in cli.logged.stderr


def test_invalid(cli, monkeypatch):
    cli.main = SHRINKY
    cli.run("")
    assert cli.failed
    assert "No command provided" in cli.logged.stderr

    cli.run("foo")
    assert cli.failed
    assert "Unknown command 'foo'" in cli.logged.stderr
    assert not cli.logged.stdout

    cli.run("ps1 foo")
    assert cli.failed
    assert "Unrecognized argument 'foo'" in cli.logged.stderr

    cli.run("ps1")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "$ "

    cli.run("ps1 -ctty")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "\x1b[32m$\x1b[39m "

    cli.run("ps1 -cfoo")
    assert cli.failed
    assert "No color set for 'foo'" in cli.logged.stderr

    assert not os.path.exists("shrinky.log")
    monkeypatch.setenv("SHRINKY_LOG", "shrinky.log")
    cli.run("ps1 -z5")
    assert cli.failed
    assert "Unknown flag 'z'" in cli.logged.stderr
    assert os.path.exists("shrinky.log")


def test_ps1(cli):
    cli.main = SHRINKY
    cli.run("ps1 -czsh -uroot -x0 -p/tmp/foo/bar/baz -v")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "❕ %F{yellow}%{\x1b[2m%}/t/f/bar/%{\x1b[22m%}baz%f%F{green}#%f "

    # User shown when not matching stated owner
    cli.run("ps1 -czsh -uuser1 -ouser2,user3 -x1")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "%F{blue}user1%f@%F{red}$%f "

    # This test's own venv
    venv_path = os.path.dirname(os.path.dirname(sys.executable))
    py_version = ".".join(str(x) for x in sys.version_info[:2])
    cli.run("ps1", "-czsh", "-x1", "-v%s" % venv_path)
    assert cli.succeeded
    output = cli.logged.stdout.contents()
    assert py_version in output

    # A fictional venv
    cli.run("ps1", "-czsh", "-vfoo/bar/.venv")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "(%F{cyan}bar%f %F{blue}None%f) %F{green}$%f "

    # Minimal args
    cli.run("ps1 -cbash")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "\\[\x1b[32m\\]$\\[\x1b[39m\\] "


def test_ps1_deep(cli, monkeypatch):
    cli.main = SHRINKY
    sample = "sample/some/very/deep/folder/with/way/too/many/characters/tests"
    runez.touch("%s/.git" % sample)
    full_path = os.path.abspath("%s/foo/bar/baz/even/more/tests" % sample)
    venv = "%s/.venv" % full_path
    runez.write("%s/bin/activate" % venv, '\nPS1="(some-very-long-venv-prompt) ${PS1:-}"')
    cli.run('ps1 -cplain -p"%s" -v"%s/.venv"' % (full_path, full_path))
    assert cli.succeeded
    expected = "(𓈓me-very-long-venv-prompt None) /𓈓/f/b/b/e/more/tests$ "
    assert cli.logged.stdout.contents() == expected

    # Simulate docker
    monkeypatch.setenv("container", "1")
    cli.run("ps1 -czsh")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "🐳 %F{green}$%f "

    # Simulate ssh
    monkeypatch.setenv("SSH_TTY", "foo")
    cli.run("ps1 -czsh")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "%F{cyan} %f%F{green}$%f "

    # Simulate coder
    monkeypatch.setenv("CODER", "foo")
    cli.run("ps1 -czsh")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "%F{cyan} %f%F{green}$%f "


def test_tmux(cli, monkeypatch):
    cli.main = SHRINKY
    monkeypatch.setenv("SHRINKY_LOG", "shrinky.log")
    assert not os.path.exists("shrinky.log")
    cli.run("tmux_short -p%s" % os.environ.get("HOME"))
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "~"
    assert os.path.exists("shrinky.log")

    cli.run("tmux_short -p~/dev/foo/bar")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "bar"

    # No git folder, no branch shown in tmux status
    cli.run("tmux_status")
    assert cli.succeeded
    assert "fg=yellow" not in cli.logged.stdout.contents()

    # Simulate git detached head
    runez.write(".git/HEAD", "g123", logger=None)
    cli.run("tmux_status")
    assert cli.succeeded
    assert "]g123#[default]" in cli.logged.stdout.contents()

    # Simulate invalid .git folder
    runez.delete(".git/HEAD", logger=None)
    runez.touch(".git/HEAD/foo", logger=None)
    cli.run("tmux_status")
    assert cli.succeeded
    logged = cli.logged.stdout.contents().strip()
    assert "|" not in logged


def test_tmux_here(cli):
    # Exercise real case (this repo)
    cli.main = SHRINKY
    project_path = runez.DEV.project_path("bin")
    cli.run("tmux_short -p%s" % project_path)
    assert cli.succeeded
    assert cli.logged.stdout.contents().endswith("/bin")

    cli.run("tmux_status -p%s" % project_path)
    assert cli.succeeded
    logged = cli.logged.stdout.contents().strip()
    assert "┆" in logged
    assert "#[default]" in logged
