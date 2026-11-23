import importlib.machinery
import importlib.util
import os
import socket
import sys
from pathlib import Path

import pytest
import runez

SHRINKY = "home/bin/gremlins/executable_shrinky"


def shrinky_module():
    script = Path(__file__).parent.parent / SHRINKY
    loader = importlib.machinery.SourceFileLoader("shrinky_module", str(script))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec
    assert spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_clean_path(cli):
    cli.main = SHRINKY
    runez.touch("foo/bar/readme.txt", logger=None)
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


def test_invalid(cli):
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

    cli.run("ps1 -cfoo")
    assert cli.failed
    assert "No color set for 'foo'" in cli.logged.stderr


def test_ps1(cli, monkeypatch):
    cli.main = SHRINKY
    cli.run("ps1")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "$ "

    # Exercise bash and tty
    cli.run("ps1 -cbash")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "\\[\x1b[32m\\]$\\[\x1b[39m\\] "

    cli.run("ps1 -ctty")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "\x1b[32m$\x1b[39m "

    # User shown when not matching stated owner
    cli.run("ps1 -czsh -uuser1 -ouser2,user3 -x1")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "%F{blue}user1%f@%F{red}$%f "

    # Root
    cli.run("ps1 -czsh -uroot -ouser1,root -x0 -p/tmp/foo/bar")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "❕ %F{yellow}%{\x1b[2m%}/tmp/foo/%{\x1b[22m%}bar %f%F{green}#%f "

    cli.run('ps1 -czsh -v"foo/bar/.venv"')
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "(%F{cyan}bar%f %F{blue}?%f) %F{green}$%f "

    # Simulate docker (lowest prio)
    monkeypatch.setenv("container", "1")
    cli.run("ps1 -czsh")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "🐳 %F{green}$%f "

    # Simulate ssh
    monkeypatch.setenv("SSH_TTY", "foo")
    hostname = socket.gethostname().partition(".")[0]
    cli.run("ps1")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == f" {hostname} $ "

    # Simulate coder (highest prio, even if SSH_TTY and container defined)
    monkeypatch.setenv("CODER", "foo")
    cli.run("ps1 -czsh")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "%F{cyan}  %f%F{green}$%f "

    # Verify logging works
    assert not os.path.exists("shrinky.log")
    monkeypatch.setenv("SHRINKY_LOG", "shrinky.log")
    cli.run("ps1 -z5")
    assert cli.failed
    assert "Unknown flag 'z'" in cli.logged.stderr
    assert os.path.exists("shrinky.log")


def test_own_venv(cli):
    cli.main = SHRINKY
    venv_path = os.path.dirname(os.path.dirname(sys.executable))
    py_version = ".".join(str(x) for x in sys.version_info[:2])
    cli.run("ps1", "-czsh", "-x1", f"-v{venv_path}")
    assert cli.succeeded
    assert py_version in cli.logged.stdout


@pytest.mark.parametrize(
    ("full_path", "expected"),
    [
        ("~", "~"),
        ("/some", "/some"),
        ("/some/foo/bar", "/some/foo/bar"),
        ("/some/foo/bar/baz", "/s/foo/bar/baz"),
        ("~/dev/foo/bar/baz", "~/d/foo/bar/baz"),
        ("/one/two/three/four/five/six", "/o/t/t/four/five/six"),
        ("/one/two/three/four/five/six/seven", "/…/t/t/f/five/six/seven"),
        ("/sample/foo/bar/baz/even/more/tests", "/…/f/b/b/even/more/tests"),
        ("~/.config/_private/projects/foo/bar/baz", "~/.c/_p/p/foo/bar/baz"),
    ],
)
def test_shortening(full_path, expected):
    module = shrinky_module()
    prefix, *parts = full_path.split("/")
    assert "/".join(module.shortened_path(prefix, parts, pivot=3, max_parts=6)) == expected


def test_tmux(cli, monkeypatch):
    cli.main = SHRINKY
    monkeypatch.setenv("SHRINKY_LOG", "shrinky.log")
    assert not os.path.exists("shrinky.log")
    cli.run("tmux_short", f"-p{os.environ.get('HOME')}")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "~"
    assert os.path.exists("shrinky.log")

    cli.run("tmux_short -p~/dev/foo/bar-omg-this-is-way-too-long")
    assert cli.succeeded
    assert cli.logged.stdout.contents() == "…this-is-way-too-long"

    # Run with regular call to `uptime`, for test coverage
    cli.run("tmux_status")
    assert cli.succeeded

    # Pretend `uptime` does not return an actual uptime (simpler `tmux_status` output)
    module = shrinky_module()
    cli.main = module.main
    monkeypatch.setattr(module, "run_program", lambda *_args: "22:52, 2 users")

    # No git folder, no branch shown in tmux status
    cli.run("tmux_status")
    assert cli.succeeded
    assert cli.logged.stdout.contents().strip() == ""

    # Simulate git branch
    runez.write("foo/my-project/.git/HEAD", "ref: refs/heads/release", logger=None)
    cli.run("tmux_status -pfoo/my-project")
    assert cli.succeeded
    assert cli.logged.stdout.contents().strip() == "#[fg=purple]release#[default]🚨"

    cli.run("tmux_short -pfoo/my-project/bar/baz")
    assert cli.succeeded
    assert cli.logged.stdout.contents().strip() == "my-project/baz"

    # Simulate git detached head
    runez.write("foo/my-project/.git/HEAD", "g124", logger=None)
    cli.run("tmux_status -pfoo/my-project")
    assert cli.succeeded
    assert cli.logged.stdout.contents().strip() == "#[fg=magenta]g124#[default]🔧"

    # Simulate invalid .git folder
    runez.touch("bad-project/.git/HEAD/foo", logger=None)
    cli.run("tmux_status -pbad-project")
    assert cli.succeeded
    assert cli.logged.stdout.contents().strip() == ""


@pytest.mark.parametrize(
    ("expected", "uptime"),
    [
        ("3d 12h", "22:52  up 3 days, 12:34, 2 users, load averages: 3.26 2.58 2.64"),
        ("2h 7m", " 10:23:45 up  2:07,  1 user"),
        ("5m", " 10:23:45 up 5 min,  load average: 0.01, 0.02, 0.00"),
        ("1m", "10:23  up 1 min, 1 user, load averages: 0.01 0.02 0.00"),
        ("2h", "10:23  up 2 hrs, 1 user, load averages: 0.01 0.02 0.00"),
        ("1d 4m", "10:23  up 1 day, 4 mins, 2 users, load averages: 0.01 0.02 0.00"),
        ("7d", "10:23  up 7 days, 1 session, load averages: 0.01 0.02 0.00"),
    ],
)
def test_uptime(expected, uptime):
    module = shrinky_module()
    actual = module.rendered_uptime(uptime, colored=False)
    assert actual == expected


def claude_statusline(cli, payload: str) -> str:
    runez.write("sample.json", payload, logger=None)
    cli.run("claude_statusline -cplain -isample.json")
    assert cli.succeeded
    return cli.logged.stdout.contents()


def test_claude_statusline(cli, monkeypatch):
    cli.main = SHRINKY
    monkeypatch.setenv("TZ", "UTC")
    sample = cli.tests_path("samples/claude-statusline.json")

    # Full line from a real capture: the one place to update when tweaking the look
    cli.run("claude_statusline", "-cplain", f"-i{sample}")
    assert cli.succeeded
    expected = "Opus 5.5 (medium)  ctx 99k (cache hit 96%)  left 5h 94% ↻05:00  7d 99% ↻Sun 18:00  cost: $1.97  1h28m"
    assert cli.logged.stdout.contents() == expected

    # Colored by default (exact colors are not pinned down here, so they can be tweaked freely)
    cli.run("claude_statusline", f"-i{sample}")
    assert cli.succeeded
    assert "\x1b[" in cli.logged.stdout.contents()

    # Ad-hoc payloads below only check the part they exercise
    # Missing fields don't break the line
    output = claude_statusline(cli, '{"model": {"id": "claude-x"}, "thinking": null, "cost": {"total_cost_usd": 25.4}}')
    assert output == "claude-x  cost: $25"

    # Fast mode, fresh session with no cost yet
    payload = '{"fast_mode": true, "model": {"id": "claude-x"}, "cost": {"total_cost_usd": 0, "total_duration_ms": 1000}}'
    output = claude_statusline(cli, payload)
    assert output == "claude-x ⚡  cost: -  0m"

    # Big context with a cold prompt cache
    payload = '{"model": {"id": "claude-x"}, "context_window": {"total_input_tokens": 320000}, "prompt_cache": {"warm": false}}'
    output = claude_statusline(cli, payload)
    assert output == "claude-x  ctx 🧊 320k"

    # Thinking turned off (possible on older models only)
    output = claude_statusline(cli, '{"model": {"id": "claude-x"}, "thinking": {"enabled": false}}')
    assert output == "🫥 claude-x"


def test_claude_statusline_failed(cli):
    cli.main = SHRINKY
    runez.write("oops.json", "oops, this not json", logger=None)
    cli.run("claude_statusline -cplain -ioops.json")
    assert cli.succeeded  # Exit code 0, so Claude Code shows the message
    assert "claude_statusline failed: JSONDecodeError" in cli.logged.stdout

    cli.run("claude_statusline -cplain -inot-there.json")
    assert cli.succeeded
    assert "claude_statusline failed: FileNotFoundError" in cli.logged.stdout


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        (None, "-"),
        (850, "850"),
        (99_034, "99k"),
        (999_499, "999k"),
        (999_500, "1.0M"),
        (1_234_567, "1.2M"),
    ],
)
def test_rendered_tokens(tokens, expected):
    assert shrinky_module().rendered_tokens(tokens) == expected


@pytest.mark.parametrize(
    ("value", "bounds", "expected"),
    [
        (None, (10, 20), "dim"),
        (None, (20, 10), "dim"),
        (5, (10, 20), "green"),
        (5, (20, 10), "red"),
        (10, (10, 20), "yellow"),
        (15, (20, 10), "yellow"),
        (20, (10, 20), "yellow"),
        (25, (10, 20), "red"),
        (25, (20, 10), "green"),
        (5, (10, 10), "green"),
        (10, (10, 10), "yellow"),
        (15, (10, 10), "red"),
    ],
)
def test_graded(value, bounds, expected):
    colors = shrinky_module().ColorSet.ttyc()
    assert colors.graded(value, bounds).name == expected


def test_composed():
    module = shrinky_module()
    bits = {k: module.ColorBit(k, f"<{k}>", f"</{k}>") for k in module.ColorSet.available}
    colors = module.ColorSet("tags", bits)
    assert colors.composed(None)("x") == "x"
    assert colors.composed("dim")("x") == "<dim>x</dim>"
    with pytest.raises(ValueError, match="Unknown color 'dimm'"):
        colors.composed("dimm")
    assert colors.composed(colors.red)("x") == "<red>x</red>"
    assert colors.composed((10, 20), 5)("x") == "<green>x</green>"
    assert colors.composed(("bold", (10, 20)), 25)("x") == "<red><bold>x</bold></red>"
