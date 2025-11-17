from pathlib import Path
import re


def _read_version_from_pyproject(path: Path) -> str | None:
    try:
        # Prefer stdlib tomllib (Python 3.11+), fall back to tomli backport for older Pythons
        try:
            import tomllib  # type: ignore
        except ModuleNotFoundError:
            import tomli as tomllib  # type: ignore

        data = tomllib.loads(path.read_text(encoding="utf-8"))
        return data.get("project", {}).get("version")
    except Exception:
        # Fallback: simple regex parse of pyproject.toml
        text = path.read_text(encoding="utf-8")
        m = re.search(r'(?m)^version\s*=\s*["\']([^"\']+)["\']', text)
        return m.group(1) if m else None


def _find_pyproject(start: Path) -> Path | None:
    current = start.resolve()
    for p in [current] + list(current.parents):
        candidate = p / "pyproject.toml"
        if candidate.exists():
            return candidate
    return None


def _get_version() -> str:
    try:
        # If the package is installed, prefer importlib.metadata
        import importlib.metadata as _im

        try:
            return _im.version("pyKRC")
        except Exception:
            pass
    except Exception:
        pass

    # Development case: parse pyproject.toml in the project tree
    try:
        here = Path(__file__).resolve().parent
        proj = _find_pyproject(here)
        if proj is not None:
            ver = _read_version_from_pyproject(proj)
            if ver:
                return ver
    except Exception:
        pass

    # Last resort
    return "0.0.0"


__version__ = _get_version()

from .control import Control
from .telemetry import Telemetry

__all__ = ["Control", "Telemetry", "__version__"]
