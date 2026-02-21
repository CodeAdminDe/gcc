"""Helpers for formatting pydantic validation errors with user-friendly hints."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError


def _strip_input_from_errors(errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return validation errors with raw input payloads removed."""
    return [{key: value for key, value in error.items() if key != "input"} for error in errors]


def _field_from_error(error: dict[str, Any]) -> str:
    """Extract leaf field name from pydantic error location tuple."""
    location = error.get("loc")
    if isinstance(location, (list, tuple)) and location:
        leaf = location[-1]
        if isinstance(leaf, str):
            return leaf
    return ""


def _input_type_name(error: dict[str, Any]) -> str:
    """Return simple input type label for hint text."""
    if "input" not in error:
        return "unknown"
    input_value = error.get("input")
    if input_value is None:
        return "null"
    return type(input_value).__name__


def _hint_for_error(error: dict[str, Any]) -> str | None:
    """Build actionable shape-conversion hints for common request mistakes."""
    error_type = str(error.get("type", ""))
    field = _field_from_error(error)
    input_type = _input_type_name(error)

    if error_type == "list_type" and field in {"details", "files_modified", "tags", "scope"}:
        return (
            f"Field '{field}' expects list[str], got {input_type}. "
            'Use an array form such as ["value"].'
        )

    if error_type in {"dict_type", "model_type"} and field == "ota_log":
        return (
            f"Field 'ota_log' expects dict[str, str], got {input_type}. "
            'Use {"observation":"...","thought":"...","action":"...","result":"..."} '
            "or omit the field."
        )

    return None


def _collect_hints(errors: list[dict[str, Any]]) -> list[str]:
    """Collect de-duplicated user-facing hints from raw pydantic errors."""
    hints: list[str] = []
    for error in errors:
        hint = _hint_for_error(error)
        if hint and hint not in hints:
            hints.append(hint)
    return hints


def build_validation_error_details(exc: ValidationError) -> dict[str, Any]:
    """Return standardized error details with hints for common schema mismatches."""
    try:
        raw_errors: list[dict[str, Any]] = exc.errors(include_context=False, include_input=True)
    except TypeError:
        raw_errors = exc.errors()

    details: dict[str, Any] = {"errors": _strip_input_from_errors(raw_errors)}
    hints = _collect_hints(raw_errors)
    if hints:
        details["hints"] = hints
    return details
