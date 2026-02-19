"""Runtime configuration helpers."""

from __future__ import annotations

import os
from collections.abc import Mapping


def get_runtime_defaults(env: Mapping[str, str] | None = None) -> tuple[str, str, int]:
    """Validate and return runtime defaults from environment variables."""
    source = env or os.environ

    transport_default = source.get("GCC_MCP_TRANSPORT", "stdio")
    allowed_transports = {"stdio", "streamable-http"}
    if transport_default not in allowed_transports:
        raise ValueError("GCC_MCP_TRANSPORT must be 'stdio' or 'streamable-http'.")

    host_default = source.get("GCC_MCP_HOST", "127.0.0.1")

    port_env = source.get("GCC_MCP_PORT", "8000")
    try:
        port_default = int(port_env)
    except ValueError as exc:
        raise ValueError("GCC_MCP_PORT must be an integer.") from exc
    if not (1 <= port_default <= 65535):
        raise ValueError("GCC_MCP_PORT must be between 1 and 65535.")

    return transport_default, host_default, port_default
