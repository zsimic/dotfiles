"""Customize the interactive Python REPL to use repo-managed history."""

from __future__ import annotations

import atexit
import os
import site
import sys
from contextlib import suppress
from pathlib import Path

DEFAULT_HISTORY_FILE = Path.home() / ".local/state/history/python.history"
ORIGINAL_INTERACTIVEHOOK = getattr(sys, "__interactivehook__", None)


def get_history_file() -> Path:
    """Return the configured history file path."""
    history = os.environ.get("PYTHON_HISTORY")
    return Path(history).expanduser() if history else DEFAULT_HISTORY_FILE


def ensure_history_dir() -> None:
    """Ensure the parent directory for the history file exists."""
    get_history_file().parent.mkdir(parents=True, exist_ok=True)


def get_builtin_history_file() -> Path | None:
    """Return the builtin history file path when the interpreter exposes it."""
    gethistoryfile = getattr(site, "gethistoryfile", None)
    if not callable(gethistoryfile):
        return None

    with suppress(OSError, RuntimeError, TypeError, ValueError):
        history_file = gethistoryfile()
        if isinstance(history_file, (str, os.PathLike)):
            return Path(history_file).expanduser()

    return None


def should_use_builtin_history() -> bool:
    """Use the interpreter's built-in hook when it already honors our history path."""
    return callable(ORIGINAL_INTERACTIVEHOOK) and get_builtin_history_file() == get_history_file()


def configure_readline() -> None:
    """Prefer the interpreter's own hook when possible, else use a fallback hook."""
    builtin_interactivehook = ORIGINAL_INTERACTIVEHOOK
    if should_use_builtin_history() and callable(builtin_interactivehook):
        ensure_history_dir()
        builtin_interactivehook()
        return

    try:
        import readline
        import rlcompleter  # noqa: F401  # Imported so readline can enable tab completion.
    except ImportError:
        return

    readline_backend = getattr(readline, "backend", None)
    readline_doc = getattr(readline, "__doc__", "")
    if readline_backend == "editline" or (readline_backend is None and readline_doc is not None and "libedit" in readline_doc):
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

    with suppress(OSError):
        readline.read_init_file()

    history_file = get_history_file()
    ensure_history_dir()

    if readline.get_current_history_length() == 0:
        with suppress(OSError):
            readline.read_history_file(str(history_file))

    def write_history() -> None:
        with suppress(OSError):
            readline.write_history_file(str(history_file))

    atexit.register(write_history)


sys.__interactivehook__ = configure_readline
