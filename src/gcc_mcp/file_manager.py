"""Low-level file system helpers used by the GCC engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .errors import ErrorCode, GCCError


class FileManager:
    """Wrapper around common text/YAML file operations."""

    def write_text(self, path: Path, content: str) -> None:
        """Write UTF-8 text to a file, creating parent directories as needed."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        except PermissionError as exc:
            raise GCCError(
                ErrorCode.PERMISSION_DENIED,
                f"Permission denied while writing {path}",
                "Check directory permissions and try again.",
            ) from exc

    def append_text(self, path: Path, content: str) -> None:
        """Append UTF-8 text to a file, creating parent directories as needed."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(content)
        except PermissionError as exc:
            raise GCCError(
                ErrorCode.PERMISSION_DENIED,
                f"Permission denied while appending {path}",
                "Check directory permissions and try again.",
            ) from exc

    def read_text(self, path: Path) -> str:
        """Read UTF-8 text from a file, returning empty text when missing."""
        try:
            return path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return ""
        except PermissionError as exc:
            raise GCCError(
                ErrorCode.PERMISSION_DENIED,
                f"Permission denied while reading {path}",
                "Check directory permissions and try again.",
            ) from exc

    def write_yaml(self, path: Path, payload: dict[str, Any]) -> None:
        """Write YAML content with stable key order to a file path."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as handle:
                yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=False)
        except PermissionError as exc:
            raise GCCError(
                ErrorCode.PERMISSION_DENIED,
                f"Permission denied while writing {path}",
                "Check directory permissions and try again.",
            ) from exc

    def read_yaml(self, path: Path) -> dict[str, Any]:
        """Read YAML mapping from disk, returning empty mapping on missing/invalid data."""
        if not path.exists():
            return {}
        try:
            with path.open("r", encoding="utf-8") as handle:
                loaded = yaml.safe_load(handle)
        except PermissionError as exc:
            raise GCCError(
                ErrorCode.PERMISSION_DENIED,
                f"Permission denied while reading {path}",
                "Check directory permissions and try again.",
            ) from exc
        if isinstance(loaded, dict):
            return loaded
        return {}
