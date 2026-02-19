# gcc-mcp

Python MCP server for the **Git Context Controller (GCC)**.  
It implements Git-inspired context operations for AI-agent workflows:

- `gcc_init`
- `gcc_commit`
- `gcc_branch`
- `gcc_merge`
- `gcc_context`
- `gcc_status`

## Quick Start

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
pytest
```

Run the MCP server (stdio transport):

```bash
gcc-mcp
```

Run with streamable HTTP (planned for remote deployment, not default for v0.1):

```bash
gcc-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Or (module mode):

```bash
python -m gcc_mcp
```

Run CLI (parity with MCP tools):

```bash
gcc-cli --help
```

Implemented CLI commands:

- `init`
- `commit`
- `branch`
- `merge`
- `context`
- `status`
- `config`
- `log`
- `list`
- `checkout`
- `delete`

Example init with secure default (`.GCC` ignored by git):

```bash
gcc-cli init \
  --directory . \
  --name "My Project" \
  --description "Context-tracked implementation"
```

Example init with explicit opt-in to track `.GCC` in git:

```bash
gcc-cli init \
  --directory . \
  --name "My Project" \
  --git-context-policy track \
  --ack-sensitive-context-risk
```

## Security Note

`.GCC/` can contain sensitive context (reasoning traces, architecture notes, and potentially
security-relevant details).  
Default behavior is `git_context_policy=ignore`, which adds `.GCC/` to `.gitignore`.  
Tracking `.GCC/` in git requires explicit acknowledgement.

Context retrieval supports optional conservative redaction:

```bash
gcc-cli context --redact-sensitive --level detailed
```

You can persist this behavior:

```bash
gcc-cli config redaction_mode true
```

## Streamable HTTP Mode

`gcc-mcp` remains stdio-first for v0.1/v0.2 local workflows.  
For remote-style testing/deployment, streamable HTTP mode is available:

```bash
gcc-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Environment variable equivalents:

- `GCC_MCP_TRANSPORT` (`stdio` or `streamable-http`)
- `GCC_MCP_HOST`
- `GCC_MCP_PORT`

## CI Quality Gates

GitHub Actions workflow: `.github/workflows/ci.yml`

Checks:

- `python -m ruff check src tests`
- `python -m pytest -q`
- `python -m py_compile src/gcc_mcp/*.py`

## Inspector & Evaluations

- MCP Inspector runbook: `docs/mcp-inspector-runbook.md`
- Evaluation pack: `eval/gcc_mcp_evaluation.xml`

## Project Layout

```text
src/gcc_mcp/
  cli.py           # gcc-cli command
  engine.py        # core GCC operations
  file_manager.py  # filesystem and YAML IO
  models.py        # pydantic request/response contracts
  server.py        # FastMCP tools
tests/
  test_cli.py
  test_engine.py
```
