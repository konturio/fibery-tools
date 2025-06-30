import os
from pathlib import Path
import stat

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "render_tasks.sh"

def test_render_tasks_script_is_executable():
    assert SCRIPT.is_file()
    assert os.access(SCRIPT, os.X_OK)
