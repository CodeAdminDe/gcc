# Audit Verification Runbook

## Purpose

Validate signed GCC audit logs for tamper evidence before incident response, compliance export, or forensic review.

## Inputs

- Audit log file (JSONL), for example: `.GCC/server-audit.jsonl`
- Signing key used when events were generated
  - Preferred source: file (`GCC_MCP_AUDIT_SIGNING_KEY_FILE` / `--audit-signing-key-file`)
  - Alternative: environment variable (`GCC_MCP_AUDIT_SIGNING_KEY`)

## Verify a log

```bash
gcc-cli audit-verify \
  --log-file .GCC/server-audit.jsonl \
  --signing-key-file .secrets/audit-signing.key
```

On success, CLI returns:

- `status=success`
- `entries_checked=<count>`
- `log_file=<path>`

On failure, CLI returns structured error payload with:

- line number of first failing event
- mismatch reason (chain, hash, or signature)

## Rotation Procedure

Current verifier accepts one signing key per verification run.

Recommended rotation flow:

1. Close current audit log file (archive as immutable artifact).
2. Rotate signing key.
3. Start a new audit log file with the new key.
4. Verify old and new files separately with their respective keys.

This preserves deterministic verification and avoids mixed-key ambiguity in one file.

## Incident Response Notes

If verification fails:

1. Preserve the original log copy immediately (read-only archive).
2. Record first failing line and error details from verifier output.
3. Compare file checksums against backup/object-store copies.
4. Correlate with deployment/key-rotation timeline to rule out key mismatch.
5. Escalate as potential tampering if mismatch cannot be explained by known operational events.
