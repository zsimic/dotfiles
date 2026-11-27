import datetime
import json
import runpy
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "home/bin/gremlins/executable_toktally"


@pytest.fixture
def toktally():
    return runpy.run_path(str(SCRIPT))


def plain(toktally):
    return toktally["ColorSet"].plain()


def tagged_colors(toktally):
    """Color set rendering colors as visible tags, to verify which color applies where"""
    bits = {k: toktally["ColorBit"](k, f"<{k}>", f"</{k}>") for k in toktally["ColorSet"].codes}
    return toktally["ColorSet"]("tags", bits)


def breakdown(model, cost, input_=0, output=0, cache_write=0, cache_read=0):
    return {
        "modelName": model,
        "cost": cost,
        "inputTokens": input_,
        "outputTokens": output,
        "cacheCreationTokens": cache_write,
        "cacheReadTokens": cache_read,
    }


SAMPLE = {
    "daily": [
        {
            "period": "2026-11-25",
            "agents": [
                {"agent": "claude", "modelBreakdowns": [breakdown("claude-opus-5-5", 40.0, 1000, 600_000, 1_400_000, 91_000_000)]},
                {"agent": "codex", "modelBreakdowns": [breakdown("gpt-6.2-astra", 3.5, 218_000, 13_000, 0, 3_100_000)]},
                {"agent": "opencode", "modelBreakdowns": [breakdown("whatever", 1.0, 1)]},
            ],
        },
        {
            "period": "2026-11-26",
            "agents": [
                {
                    "agent": "claude",
                    "modelBreakdowns": [
                        breakdown("claude-opus-5-5", 2.0, 300, 80_000, 160_000, 13_000_000),
                        breakdown("claude-haiku-5-5", 0.25, 60, 40_000, 520_000, 1_380_000),
                    ],
                }
            ],
        },
    ]
}


def fake_ccusage(toktally, monkeypatch, report=None, error=None):
    calls = []

    def run(cmd, **_):
        calls.append(cmd)
        if error:
            raise error

        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(report or {}))

    monkeypatch.setattr(toktally["subprocess"], "run", run)
    return calls


@pytest.mark.parametrize(
    ("count", "expected"),
    [
        (0, "0"),
        (999, "999"),
        (1000, "1K"),
        (1234, "1.2K"),
        (9_960, "10K"),
        (146_234_567, "146M"),
        (2_500_000, "2.5M"),
        (3_000_000_000, "3G"),
        (5 * 10**18, "5000P"),
    ],
)
def test_with_units(toktally, count, expected):
    assert toktally["with_units"](count) == expected


def test_since_date(toktally):
    assert toktally["since_date"]("2026-11-01") == datetime.date(2026, 11, 1)
    assert toktally["since_date"]("20261101") == datetime.date(2026, 11, 1)
    with pytest.raises(Exception, match="invalid date 'nope'"):
        toktally["since_date"]("nope")


def test_report_sums_per_model_and_filters_agents(toktally):
    report = toktally["UsageReport"](("claude",), datetime.date(2026, 11, 1))
    report.add_ccusage_report(SAMPLE)
    usages = report.sorted_usages()
    assert [(u.agent, u.model) for u in usages] == [("claude", "claude-opus-5-5"), ("claude", "claude-haiku-5-5")]
    opus = usages[0]
    assert opus.cost == 42.0
    assert opus.input == 1300
    assert opus.total == 1300 + 680_000 + 1_560_000 + 104_000_000


def test_rendered(toktally):
    report = toktally["UsageReport"](("codex", "claude"), datetime.date(2026, 11, 1))
    assert report.rendered(plain(toktally)) == "Token usage since 2026-11-01 (codex, claude): nothing was eaten"

    report.add_ccusage_report(SAMPLE)
    lines = report.rendered(plain(toktally)).splitlines()
    assert lines[0] == "Token usage since 2026-11-01 (codex, claude)"
    assert lines[2].split() == ["Agent", "Model", "Input", "Output", "Cache", "write", "Cache", "read", "Total", "Cost"]
    assert lines[4].split() == ["claude", "claude-opus-5-5", "1.3K", "680K", "1.6M", "104M", "106M", "$42.00"]
    assert lines[5].split() == ["codex", "gpt-6.2-astra", "218K", "13K", "0", "3.1M", "3.3M", "$3.50"]
    assert lines[6].split() == ["claude", "claude-haiku-5-5", "60", "40K", "520K", "1.4M", "1.9M", "$0.25"]
    assert lines[7].startswith("------")
    assert lines[8].split() == ["Total", "219K", "733K", "2.1M", "108M", "112M", "$45.75"]
    assert "whatever" not in report.rendered(plain(toktally))


def test_rendered_colors(toktally):
    report = toktally["UsageReport"](("codex", "claude"), datetime.date(2026, 11, 1))
    report.add_ccusage_report(SAMPLE)
    report.usages["codex", "gpt-6.2-astra"].cost = 250
    report.usages["claude", "claude-haiku-5-5"].cost = 150
    lines = report.rendered(tagged_colors(toktally)).splitlines()
    assert lines[0] == "<bold>Token usage since 2026-11-01 (codex, claude)</bold>"
    assert lines[2].startswith("<bold>Agent")
    assert lines[3].startswith("<dim>------")
    assert lines[4].endswith("<red>$250.00</red>")  # Sorted by cost
    assert lines[5].endswith("<yellow>$150.00</yellow>")
    assert lines[6].endswith("<green> $42.00</green>")
    assert lines[8].startswith("<bold>")
    assert lines[8].endswith("$442.00</bold>")


@pytest.mark.parametrize(("cost", "expected"), [(0, "green"), (99.99, "green"), (100, "yellow"), (200, "yellow"), (200.01, "red")])
def test_graded(toktally, cost, expected):
    assert toktally["ColorSet"].tty().graded(cost, (100, 200)).name == expected


def test_color_sets(toktally, monkeypatch):
    color_set = toktally["ColorSet"]
    assert color_set.tty().red("x") == "\x1b[31mx\x1b[39m"
    assert color_set.tty().bold("x") == "\x1b[1mx\x1b[22m"
    assert color_set.plain().red("x") == "x"
    assert color_set.for_output(True).name == "tty"
    assert color_set.for_output(False).name == "plain"

    monkeypatch.setattr(toktally["sys"].stdout, "isatty", lambda: True, raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)
    assert color_set.for_output(None).name == "tty"
    monkeypatch.setenv("NO_COLOR", "1")
    assert color_set.for_output(None).name == "plain"


def test_rendered_single_model_has_no_total(toktally):
    report = toktally["UsageReport"](("codex",), datetime.date(2026, 11, 1))
    report.add_ccusage_report(SAMPLE)
    lines = report.rendered(plain(toktally)).splitlines()
    assert len(lines) == 5
    assert "Total" not in lines[-1]


def test_main_defaults(toktally, monkeypatch, capsys):
    calls = fake_ccusage(toktally, monkeypatch, SAMPLE)
    toktally["main"]([])  # Captured stdout is not a tty: no colors
    since = datetime.datetime.now().astimezone().date() - datetime.timedelta(days=29)
    assert calls == [["ccusage", "daily", "--json", "--by-agent", "--since", since.strftime("%Y%m%d")]]
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == f"Token usage since {since} (all agents)"
    assert [line.split()[1] for line in lines[4:-2]] == ["claude-opus-5-5", "gpt-6.2-astra", "whatever", "claude-haiku-5-5"]
    assert lines[-1].endswith("$46.75")


def test_main_agent_and_since(toktally, monkeypatch, capsys):
    calls = fake_ccusage(toktally, monkeypatch, SAMPLE)
    toktally["main"](["-a", "codex,claude", "--since", "2026-11-20", "--color"])
    assert calls[0][-1] == "20261120"
    output = capsys.readouterr().out
    assert output.startswith("\x1b[1mToken usage since 2026-11-20 (codex, claude)")
    assert "gpt-6.2-astra" in output
    assert "claude-opus-5-5" in output
    assert "opencode" not in output
    assert output.splitlines()[-1].endswith("$45.75\x1b[22m")


def test_main_agent_accepts_reported_names(toktally, monkeypatch, capsys):
    fake_ccusage(toktally, monkeypatch, SAMPLE)
    toktally["main"](["--agent", "opencode", "--no-color"])
    output = capsys.readouterr().out
    assert "whatever" in output
    assert "gpt-6.2-astra" not in output
    assert "claude-opus-5-5" not in output


def test_main_model_filter(toktally, monkeypatch, capsys):
    fake_ccusage(toktally, monkeypatch, SAMPLE)
    toktally["main"](["-mgpt", "--no-color"])
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].endswith("(all agents, model contains 'gpt')")
    assert len(lines) == 5
    assert lines[-1].split()[:2] == ["codex", "gpt-6.2-astra"]


@pytest.mark.parametrize("args", [["-m"], ["--model"], ["-m", ""]])
def test_main_model_sort(toktally, monkeypatch, capsys, args):
    fake_ccusage(toktally, monkeypatch, SAMPLE)
    toktally["main"]([*args, "--no-color"])
    lines = capsys.readouterr().out.splitlines()
    assert [line.split()[1] for line in lines[4:-2]] == ["claude-haiku-5-5", "claude-opus-5-5", "gpt-6.2-astra", "whatever"]
    assert lines[-1].endswith("$46.75")


def test_main_combines_agent_and_model_filters(toktally, monkeypatch, capsys):
    fake_ccusage(toktally, monkeypatch, SAMPLE)
    toktally["main"](["-a", "claude,opencode", "--model", "-", "--no-color"])
    lines = capsys.readouterr().out.splitlines()
    assert [line.split()[:2] for line in lines[4:6]] == [
        ["claude", "claude-haiku-5-5"],
        ["claude", "claude-opus-5-5"],
    ]
    assert len(lines) == 8
    assert lines[-1].endswith("$42.25")


@pytest.mark.parametrize(
    ("args", "error"),
    [
        (["claude"], "unrecognized arguments: claude"),
        (["-a", "codex,"], "expected comma-separated agent names"),
        (["--days", "3", "--since", "2026-11-01"], "not allowed with argument"),
    ],
)
def test_main_rejects_invalid_arguments(toktally, capsys, args, error):
    with pytest.raises(SystemExit):
        toktally["main"](args)

    assert error in capsys.readouterr().err


def test_ccusage_missing(toktally, monkeypatch):
    fake_ccusage(toktally, monkeypatch, error=FileNotFoundError("ccusage"))
    with pytest.raises(SystemExit, match="ccusage is not installed"):
        toktally["main"]([])


def test_ccusage_fails(toktally, monkeypatch):
    fake_ccusage(toktally, monkeypatch, error=subprocess.CalledProcessError(1, "ccusage", stderr="boom\n"))
    with pytest.raises(SystemExit, match="failed:\nboom"):
        toktally["main"]([])
