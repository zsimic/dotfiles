import os

ZTERM = "home/bin/executable_zterm"


def test_iterm(cli):
    cli.main = ZTERM
    cli.run("-v", "i", "foo")
    assert cli.failed
    assert "No profile 'foo' in iterm2 plist" in cli.logged.stderr

    cli.run("-nv", "test")
    assert cli.succeeded
    assert "Would exec: exec open -na Ghostty" in cli.logged.stdout
    assert "Resetting env vars" in cli.logged.stderr

    cli.run("-n", "i", "asciinema")
    assert cli.succeeded
    assert 'create window with profile "asciinema"' in cli.logged.stdout

    assert "PYTEST_CURRENT_TEST" in os.environ
    cli.run("show-env")
    assert cli.succeeded
    assert "LOGNAME:" not in cli.logged.stdout
    assert "PYTEST_CURRENT_TEST" not in cli.logged.stdout
