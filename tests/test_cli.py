from __future__ import annotations

import json
from pathlib import Path

from gcc_mcp.cli import main


def _run_cli_json(args: list[str], capsys) -> dict:
    exit_code = main(args + ["--json"])
    assert exit_code in (0, 1)
    output = capsys.readouterr().out
    return {"exit_code": exit_code, "payload": json.loads(output)}


def test_cli_init_and_status(tmp_path: Path, capsys) -> None:
    init_result = _run_cli_json(
        [
            "init",
            "--directory",
            str(tmp_path),
            "--name",
            "CLI Project",
            "--description",
            "Parity test",
            "--goals",
            "goal-a,goal-b",
        ],
        capsys,
    )
    assert init_result["exit_code"] == 0
    assert init_result["payload"]["status"] == "success"
    assert init_result["payload"]["git_context_policy"] == "ignore"

    status_result = _run_cli_json(["status", "--directory", str(tmp_path)], capsys)
    assert status_result["exit_code"] == 0
    assert status_result["payload"]["status"] == "success"
    assert status_result["payload"]["project_name"] == "CLI Project"


def test_cli_track_policy_requires_ack(tmp_path: Path, capsys) -> None:
    result = _run_cli_json(
        [
            "init",
            "--directory",
            str(tmp_path),
            "--name",
            "CLI Project",
            "--git-context-policy",
            "track",
        ],
        capsys,
    )
    assert result["exit_code"] == 1
    assert result["payload"]["status"] == "error"
    assert result["payload"]["error_code"] == "INVALID_INPUT"


def test_cli_parity_commands(tmp_path: Path, capsys) -> None:
    init_result = _run_cli_json(
        [
            "init",
            "--directory",
            str(tmp_path),
            "--name",
            "CLI Project",
        ],
        capsys,
    )
    assert init_result["exit_code"] == 0

    branch_result = _run_cli_json(
        [
            "branch",
            "exp-a",
            "--directory",
            str(tmp_path),
            "--description",
            "Experiment A",
        ],
        capsys,
    )
    assert branch_result["payload"]["status"] == "success"

    checkout_main = _run_cli_json(
        [
            "checkout",
            "main",
            "--directory",
            str(tmp_path),
        ],
        capsys,
    )
    assert checkout_main["payload"]["status"] == "success"
    assert checkout_main["payload"]["current_branch"] == "main"

    config_set = _run_cli_json(
        [
            "config",
            "--directory",
            str(tmp_path),
            "log_level",
            "DEBUG",
        ],
        capsys,
    )
    assert config_set["payload"]["status"] == "success"
    assert config_set["payload"]["config"]["log_level"] == "DEBUG"

    list_result = _run_cli_json(["list", "--directory", str(tmp_path)], capsys)
    assert list_result["payload"]["status"] == "success"
    assert list_result["payload"]["count"] == 2

    _run_cli_json(
        [
            "checkout",
            "exp-a",
            "--directory",
            str(tmp_path),
        ],
        capsys,
    )
    commit_result = _run_cli_json(
        [
            "commit",
            "--directory",
            str(tmp_path),
            "--message",
            "Experiment result",
            "--type",
            "feature",
            "--tags",
            "experiment,perf",
        ],
        capsys,
    )
    assert commit_result["payload"]["status"] == "success"

    log_result = _run_cli_json(
        [
            "log",
            "exp-a",
            "--directory",
            str(tmp_path),
            "--type",
            "feature",
            "--tags",
            "perf",
        ],
        capsys,
    )
    assert log_result["payload"]["status"] == "success"
    assert log_result["payload"]["count"] == 1
    assert log_result["payload"]["entries"][0]["message"] == "Experiment result"

    context_result = _run_cli_json(
        [
            "context",
            "--directory",
            str(tmp_path),
            "--level",
            "detailed",
            "--redact-sensitive",
        ],
        capsys,
    )
    assert context_result["payload"]["status"] == "success"
    assert context_result["payload"]["redaction_applied"] is True

    _run_cli_json(
        [
            "checkout",
            "main",
            "--directory",
            str(tmp_path),
        ],
        capsys,
    )
    delete_result = _run_cli_json(
        [
            "delete",
            "exp-a",
            "--directory",
            str(tmp_path),
            "--archive",
        ],
        capsys,
    )
    assert delete_result["payload"]["status"] == "success"


def test_cli_log_invalid_since_rejected(tmp_path: Path, capsys) -> None:
    _run_cli_json(
        [
            "init",
            "--directory",
            str(tmp_path),
            "--name",
            "CLI Project",
        ],
        capsys,
    )
    _run_cli_json(
        [
            "commit",
            "--directory",
            str(tmp_path),
            "--message",
            "Baseline",
        ],
        capsys,
    )
    result = _run_cli_json(
        [
            "log",
            "--directory",
            str(tmp_path),
            "--since",
            "2026-02-99",
        ],
        capsys,
    )
    assert result["exit_code"] == 1
    assert result["payload"]["status"] == "error"
    assert result["payload"]["error_code"] == "INVALID_INPUT"


def test_cli_config_non_json_output_shows_values(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "init",
            "--directory",
            str(tmp_path),
            "--name",
            "CLI Project",
        ]
    )
    assert exit_code == 0
    capsys.readouterr()

    exit_code = main(["config", "--directory", str(tmp_path), "--list"])
    assert exit_code == 0
    output = capsys.readouterr().out
    assert "config:" in output
    assert "project_name: CLI Project" in output
