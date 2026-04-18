import importlib.util
import sys
from pathlib import Path

STARTUP = Path(__file__).resolve().parent.parent / "home/dot_config/python/startup.py"


def load_startup_module():
    spec = importlib.util.spec_from_file_location("python_startup_module", STARTUP)
    assert spec and spec.loader  # noqa: PT018
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeReadline:
    def __init__(self, *, doc="libedit", history_length=0):
        self.__doc__ = doc
        self.history_length = history_length
        self.bindings = []
        self.init_file_reads = 0
        self.history_reads = []
        self.history_writes = []

    def parse_and_bind(self, binding):
        self.bindings.append(binding)

    def read_init_file(self):
        self.init_file_reads += 1

    def get_current_history_length(self):
        return self.history_length

    def read_history_file(self, path):
        self.history_reads.append(path)

    def write_history_file(self, path):
        self.history_writes.append(path)


def test_startup_installs_interactive_hook(monkeypatch):
    sentinel = object()
    monkeypatch.setattr(sys, "__interactivehook__", sentinel, raising=False)
    module = load_startup_module()

    assert module.ORIGINAL_INTERACTIVEHOOK is sentinel
    assert sys.__interactivehook__ is module.configure_readline


def test_startup_uses_custom_history_file(monkeypatch, tmp_path):
    module = load_startup_module()
    fake_readline = FakeReadline()
    registered = []
    history_file = tmp_path / ".local/state/history/python.history"

    monkeypatch.setenv("PYTHON_HISTORY", str(history_file))
    monkeypatch.setattr(module, "ORIGINAL_INTERACTIVEHOOK", None)
    monkeypatch.delattr(module.site, "gethistoryfile", raising=False)
    monkeypatch.setattr(module.atexit, "register", registered.append)
    monkeypatch.setitem(sys.modules, "readline", fake_readline)
    monkeypatch.setitem(sys.modules, "rlcompleter", object())

    module.configure_readline()

    assert fake_readline.bindings == ["bind ^I rl_complete"]
    assert fake_readline.init_file_reads == 1
    assert fake_readline.history_reads == [str(history_file)]
    assert history_file.parent.is_dir()
    assert len(registered) == 1

    registered[0]()
    assert fake_readline.history_writes == [str(history_file)]


def test_startup_delegates_to_builtin_history_support(monkeypatch, tmp_path):
    module = load_startup_module()
    history_file = tmp_path / ".local/state/history/python.history"
    calls = []

    monkeypatch.setenv("PYTHON_HISTORY", str(history_file))
    monkeypatch.setattr(module, "ORIGINAL_INTERACTIVEHOOK", lambda: calls.append("builtin"))
    monkeypatch.setattr(module.site, "gethistoryfile", lambda: str(history_file), raising=False)

    module.configure_readline()

    assert calls == ["builtin"]
    assert history_file.parent.is_dir()
