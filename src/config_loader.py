import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Tuple


def load_config() -> ModuleType:
    """Return the ``config`` module ensuring project root is in ``sys.path``."""
    try:
        import config  # type: ignore
    except ImportError:
        root = Path(__file__).resolve().parents[1]
        if str(root) not in sys.path:
            sys.path.append(str(root))
        try:
            import config  # type: ignore
        except ImportError as exc:  # pragma: no cover - configuration must be supplied
            raise SystemExit(
                "Missing config.py. Copy config.py.example and provide real values."
            ) from exc
    return config


def import_config(*names: str) -> Tuple[Any, ...]:
    """Import selected configuration values and return them."""
    cfg = load_config()
    return tuple(getattr(cfg, name) for name in names)
