import importlib.util
import plistlib
from importlib.machinery import SourceFileLoader
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
YO_MUX_PATH = PROJECT_ROOT / "home/bin/executable_yo-mux"
loader = SourceFileLoader("executable_yo_mux", str(YO_MUX_PATH))
spec = importlib.util.spec_from_loader(loader.name, loader)
yo_mux = importlib.util.module_from_spec(spec)
loader.exec_module(yo_mux)


def test_find_iterm_profile_in_new_bookmarks():
    plist_path = PROJECT_ROOT / "resources/darwin/iterm2/com.googlecode.iterm2.plist"
    with plist_path.open("rb") as fh:
        prefs = plistlib.load(fh)

    profile = yo_mux.find_iterm_profile_in_prefs(prefs, "asciinema")

    assert profile["Name"] == "asciinema"


def test_find_iterm_profile_in_legacy_profiles():
    prefs = {
        "Profiles": [
            {"Name": "main"},
            {"Name": "legacy"},
        ]
    }

    profile = yo_mux.find_iterm_profile_in_prefs(prefs, "legacy")

    assert profile["Name"] == "legacy"


def test_find_iterm_profile_missing():
    prefs = {"New Bookmarks": [{"Name": "main"}]}

    assert yo_mux.find_iterm_profile_in_prefs(prefs, "missing") is None
