import pathlib
import py_compile

SRC_DIR = pathlib.Path(__file__).resolve().parents[1] / "src"

def test_sources_compile():
    """Compile all Python sources from src directory."""
    for path in SRC_DIR.glob("*.py"):
        py_compile.compile(path, doraise=True)
