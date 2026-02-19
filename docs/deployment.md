# Deployment Notes

## Transport Strategy

- Default transport: `stdio` (recommended for local agent integrations).
- Remote/testing transport: `streamable-http` (already implemented behind runtime flags).

## Runtime Configuration

### CLI flags

```bash
gcc-mcp --transport stdio
gcc-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

### Environment variables

- `GCC_MCP_TRANSPORT` (`stdio` or `streamable-http`)
- `GCC_MCP_HOST` (default `127.0.0.1`)
- `GCC_MCP_PORT` (default `8000`)

Example:

```bash
export GCC_MCP_TRANSPORT=streamable-http
export GCC_MCP_HOST=0.0.0.0
export GCC_MCP_PORT=8000
gcc-mcp
```

## Security Considerations

- `.GCC/` may contain sensitive context and should stay ignored by default.
- For remote deployments, ensure network-level controls (firewalls, private network, auth proxy).
- Use `redaction_mode=true` where broad context access is exposed.

## Production Hardening Backlog

- Introduce an authn/authz layer for remote endpoints.
- Add structured request/response access logs with sensitive-field filtering.
- Provide rate limiting and reverse-proxy guidance.
