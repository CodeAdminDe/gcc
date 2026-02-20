from __future__ import annotations

import pytest

pytest.importorskip("mcp")

from gcc_mcp import server


def test_register_tool_uses_annotations_when_supported(monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    class FakeMCP:
        def tool(self, **kwargs: object):
            calls.append(dict(kwargs))

            def _decorator(func):
                return func

            return _decorator

    monkeypatch.setattr(server, "mcp", FakeMCP())

    decorator = server._register_tool({"readOnlyHint": True})

    def _sample() -> str:
        return "ok"

    wrapped = decorator(_sample)
    assert wrapped() == "ok"
    assert calls == [{"annotations": {"readOnlyHint": True}}]


def test_register_tool_falls_back_when_annotations_are_unsupported(monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    class FakeMCP:
        def tool(self, **kwargs: object):
            calls.append(dict(kwargs))
            if "annotations" in kwargs:
                raise TypeError("tool() got an unexpected keyword argument 'annotations'")

            def _decorator(func):
                return func

            return _decorator

    monkeypatch.setattr(server, "mcp", FakeMCP())

    decorator = server._register_tool({"readOnlyHint": True})

    def _sample() -> str:
        return "ok"

    wrapped = decorator(_sample)
    assert wrapped() == "ok"
    assert calls == [
        {"annotations": {"readOnlyHint": True}},
        {},
    ]


def test_register_tool_re_raises_unrelated_type_errors(monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    class FakeMCP:
        def tool(self, **kwargs: object):
            calls.append(dict(kwargs))
            raise TypeError("tool() got an unexpected keyword argument 'foo'")

    monkeypatch.setattr(server, "mcp", FakeMCP())

    decorator = server._register_tool({"readOnlyHint": True})

    def _sample() -> str:
        return "ok"

    with pytest.raises(TypeError, match="foo"):
        decorator(_sample)
    assert calls == [{"annotations": {"readOnlyHint": True}}]
