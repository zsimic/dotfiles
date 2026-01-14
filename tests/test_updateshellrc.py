import os

import executable_updateshellrc as updateshellrc
import runez


def test_dryrun(cli):
    # Snippet given as positional arg
    cli.run("-n", "my-bash.rc", "some\ncontent", main=updateshellrc.main)
    assert cli.succeeded
    assert "[DRYRUN] Would update my-bash.rc, contents:" in cli.logged.stderr
    assert "## -- Added by updateshellrc.py -- DO NOT MODIFY THIS SECTION" in cli.logged.stderr
    assert "some\ncontent\n## -- end of addition" in cli.logged.stderr

    # Multi-line comment is not accepted
    cli.run("-n", "my-bash.rc", "some\ncontent", "-c", "multiple\n\nlines", main=updateshellrc.main)
    assert cli.failed
    assert "Provide maximum one line of comment, got 3 lines:\nmultiple\n\nlines" in cli.logged.stderr.contents()


EXPECTED_REGEN = """
Updating samples/bashrc
Contents:
# example bashrc file
alias ls='ls -FGh'

## -- Added by my-test-app -- DO NOT MODIFY THIS SECTION
local_bin=~/.local/bin
if [[ $PATH != *"$local_bin"* && -d $1 ]]; then
    export PATH=$local_bin:$PATH
fi
## -- end of addition by my-test-app --

alias foo=~/bar
"""


EXPECTED_EMPTIED_REGEN = """
# example bashrc file
alias ls='ls -FGh'


alias foo=~/bar

## -- Added by my-test-app -- DO NOT MODIFY THIS SECTION
local_bin=~/.local/bin
if [[ $PATH != *"$local_bin"* && -d $1 ]]; then
    export PATH=$local_bin:$PATH
fi
## -- end of addition by my-test-app --
"""


def last_n_lines(n, text):
    return text.splitlines()[-n:]


def test_samples(cli):
    sample_dir = os.path.join(runez.DEV.project_folder, "tests/samples")
    runez.copy(sample_dir, "samples", logger=None)

    cli.run("-v", "samples/bashrc", "file:samples/ensure-path", "-m", "my-test-app", main=updateshellrc.main)
    assert cli.succeeded
    assert "Section has not changed, not modifying 'samples/bashrc'" in cli.logged.stderr.contents()

    cli.run("-n", "samples/bashrc", "_empty_", "-m", "my-test-app", main=updateshellrc.main)
    assert cli.succeeded
    lines = last_n_lines(5, cli.logged.stderr.contents())
    assert lines == [
        "[DRYRUN] Would update samples/bashrc, contents:",
        "# example bashrc file",
        "alias ls='ls -FGh'",
        "",
        "alias foo=~/bar",
    ]
    assert "[DRYRUN] Would update samples/bashrc" in cli.logged.stderr
    assert "## -- Added by my-test-app" not in cli.logged

    cli.run("-n", "samples/bashrc", "foo\\nbar", "-m", "my-test-app", main=updateshellrc.main)
    assert cli.succeeded
    assert "[DRYRUN] Would update samples/bashrc" in cli.logged.stderr
    assert "foo\nbar\n## -- end of addition" in cli.logged

    cli.run("-v", "--force", "samples/bashrc", "file:samples/ensure-path", "-m", "my-test-app", main=updateshellrc.main)
    assert cli.succeeded
    actual_lines = last_n_lines(13, cli.logged.stderr.contents())
    assert actual_lines == EXPECTED_REGEN.strip().splitlines()

    cli.run("samples/bashrc", "file:samples/ensure-path", "-m", "my-test-app", main=updateshellrc.main)
    assert cli.succeeded
    assert "Section has not changed, not modifying 'samples/bashrc'" in cli.logged

    cli.run("samples/bashrc", "_empty_", "-m", "my-test-app", main=updateshellrc.main)
    assert cli.succeeded
    assert "Updating samples/bashrc" in cli.logged.stderr.contents()
    contents = list(runez.readlines("samples/bashrc"))
    assert contents == ["# example bashrc file", "alias ls='ls -FGh'", "", "", "alias foo=~/bar"]

    cli.run("samples/bashrc", "file:samples/ensure-path", "-m", "my-test-app", main=updateshellrc.main)
    assert cli.succeeded
    assert "Updating samples/bashrc" in cli.logged.stderr.contents()
    contents = runez.readlines("samples/bashrc")
    contents = "\n".join(contents)
    assert contents == EXPECTED_EMPTIED_REGEN.strip()
