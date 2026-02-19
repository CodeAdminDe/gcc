from __future__ import annotations

import pytest

from gcc_mcp.runtime import get_runtime_defaults


def test_validated_runtime_defaults_ok(monkeypatch) -> None:
    monkeypatch.setenv("GCC_MCP_TRANSPORT", "streamable-http")
    monkeypatch.setenv("GCC_MCP_HOST", "0.0.0.0")
    monkeypatch.setenv("GCC_MCP_PORT", "9000")

    transport, host, port = get_runtime_defaults()
    assert transport == "streamable-http"
    assert host == "0.0.0.0"
    assert port == 9000


def test_validated_runtime_defaults_invalid_transport(monkeypatch) -> None:
    monkeypatch.setenv("GCC_MCP_TRANSPORT", "tcp")
    with pytest.raises(ValueError):
        get_runtime_defaults()


def test_validated_runtime_defaults_invalid_port(monkeypatch) -> None:
    monkeypatch.setenv("GCC_MCP_TRANSPORT", "stdio")
    monkeypatch.setenv("GCC_MCP_PORT", "not-a-number")
    with pytest.raises(ValueError):
        get_runtime_defaults()


def test_validated_runtime_defaults_explicit_empty_env_mapping(monkeypatch) -> None:
    monkeypatch.setenv("GCC_MCP_TRANSPORT", "streamable-http")
    monkeypatch.setenv("GCC_MCP_HOST", "10.0.0.1")
    monkeypatch.setenv("GCC_MCP_PORT", "9090")

    transport, host, port = get_runtime_defaults(env={})
    assert transport == "stdio"
    assert host == "127.0.0.1"
    assert port == 8000


@pytest.mark.parametrize("port", ["0", "65536"])
def test_validated_runtime_defaults_invalid_port_range(port: str) -> None:
    with pytest.raises(ValueError):
        get_runtime_defaults(
            env={
                "GCC_MCP_TRANSPORT": "stdio",
                "GCC_MCP_HOST": "127.0.0.1",
                "GCC_MCP_PORT": port,
            }
        )
