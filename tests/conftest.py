import sys
from pathlib import Path

from runez.conftest import cli  # noqa: F401, fixture

# Temp hack: this allows to import `.py` files from the `bin/` folder
PROJECT_PATH = Path(__file__).parent.parent / "home/bin"
sys.path.insert(0, str(PROJECT_PATH))
