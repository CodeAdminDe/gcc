# MCP Inspector Runbook

## Purpose

Validate tool discoverability and behavioral correctness with MCP Inspector.

## Prerequisites

- Node.js 20+
- Python environment with project installed

## Start server (stdio)

```bash
gcc-mcp
```

## Launch inspector

```bash
npx @modelcontextprotocol/inspector
```

Use stdio mode and point to:

- Command: `gcc-mcp`
- Args: none

## Verification Checklist

1. Ensure all tools are listed:
   - `gcc_init`, `gcc_commit`, `gcc_branch`, `gcc_merge`, `gcc_context`, `gcc_status`
2. Validate init security contract:
   - `git_context_policy=ignore` works by default.
   - `git_context_policy=track` fails without risk acknowledgement.
3. Validate context filters:
   - `level`, `scope`, `since`, `tags`, `format` operate as expected.
4. Validate redaction:
   - `redact_sensitive=true` returns redacted payloads.
5. Validate error contract:
   - all failures contain `status`, `error_code`, `message`, `suggestion`, `details`.
   - timeout-classified failures include `error_code=TIMEOUT` and `correlation_id`.

## Resource-vs-Tool Discovery Notes

- MCP resources and MCP tools are separate capability surfaces.
- An empty resource listing does **not** imply the `gcc` server is unavailable.
- For `gcc-mcp`, tool availability is the primary operational signal.

## Troubleshooting

If `list_mcp_resources(server=\"gcc\")` returns an empty list:

1. Verify the server is reachable and tools are visible in Inspector.
2. Perform a direct tool ping instead of relying on resource listing:
   - call `gcc_status` with a known GCC-enabled directory.
3. If no GCC-enabled directory is available yet, run:
   - `gcc_init` on a temporary directory, then
   - `gcc_status` against that same directory.
4. If tool calls fail, inspect auth/path configuration (`GCC_MCP_AUTH_*`, `GCC_MCP_PATH_MAP`, `GCC_MCP_ALLOWED_ROOTS`).

## Scripted smoke harness

Use:

```bash
scripts/run_mcp_inspector.sh
```

This script performs local quality checks and prints commands for launching inspector.
