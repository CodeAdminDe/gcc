---
name: git-context-controller
description: Use this skill when working on the GCC codebase or operating GCC through MCP/CLI. Covers tool and CLI parity, secure context initialization, schema contracts, runtime hardening, and project workflows.
---

# Git Context Controller (GCC) Skill

## Overview

Git Context Controller (GCC) is a Python MCP server and CLI that manages structured agent context in a Git-inspired branch model under `.GCC/`.

Primary entrypoints:

- `gcc-mcp` (MCP server)
- `gcc-cli` (CLI parity)
- `python -m gcc_mcp` (module entrypoint)

## Use This Skill When

- implementing or reviewing `src/gcc_mcp/*`
- adding/changing MCP tools and keeping CLI parity
- operating branch/commit/context flows for long-running tasks
- hardening remote MCP deployments (`streamable-http`, auth, audit, strict mode)

## Core Runtime Facts

- default transport: `stdio`
- remote/testing transport: `streamable-http`
- security profiles: `baseline` (default), `strict`
- auth modes (`streamable-http`): `off`, `token`, `trusted-proxy-header`, `oauth2`

## Security and Policy Contracts

- `.GCC/` is ignored by default (`git_context_policy=ignore`).
- tracking `.GCC/` requires explicit opt-in:
  - `git_context_policy=track`
  - `acknowledge_sensitive_data_risk=true`
- in `strict` + `streamable-http`:
  - `auth-mode` must be non-`off`
  - `audit-log-file` must be configured
  - audit signing key material must be present
- prefer env vars or key files for secrets; avoid direct CLI secret flags in shared environments.

## MCP Tool Set

- `gcc_init`
- `gcc_commit`
- `gcc_branch`
- `gcc_merge`
- `gcc_context`
- `gcc_status`
- `gcc_log`
- `gcc_list`
- `gcc_checkout`
- `gcc_delete`
- `gcc_config_get`
- `gcc_config_set`
- `gcc_config_list`

## CLI Parity Commands

- `init`
- `commit`
- `branch`
- `merge`
- `context`
- `status`
- `log`
- `list`
- `checkout`
- `delete`
- `config`
- `audit-verify`

## Schema Shape Reminders (Frequent Integration Pitfalls)

- `gcc_commit.details`: `list[str]`
- `gcc_commit.files_modified`: `list[str]`
- `gcc_commit.tags`: `list[str]`
- `gcc_commit.ota_log`: `dict[str, str]` (or omitted)
- `gcc_branch.tags`: `list[str]`
- `gcc_context.scope`: `list[str]`

If wrong shapes are provided, GCC returns validation errors with actionable `details.hints`.

## Recommended Workflow

1. Initialize repository context:
   - `gcc-cli init --directory <repo> --name "<project>"`
2. Create branch for alternative strategy:
   - `gcc-cli branch <name> --directory <repo> --description "<purpose>"`
3. Checkpoint milestones:
   - `gcc-cli commit --directory <repo> --message "<summary>"`
4. Recover context / status:
   - `gcc-cli context --directory <repo> --level detailed`
   - `gcc-cli status --directory <repo>`
5. Merge completed branch:
   - `gcc-cli merge <source> --directory <repo> --summary "<merge-summary>"`

## Development and Verification

```bash
python -m ruff check src tests
python -m pytest -q
```

Runtime diagnostics:

```bash
gcc-mcp --check-config
gcc-mcp --print-effective-config
```

## Documentation Map

- installation: `docs/installation.md`
- first-time onboarding (repo 1, repo 2+): `docs/onboarding.md`
- deployment and remote hardening: `docs/deployment.md`
- security model: `docs/security-model.md`
- production readiness: `docs/production-readiness-checklist.md`

## Notes About Source Alignment

This repository `SKILL.md` is aligned to the historical Notion skill page and updated to match current GCC implementation details and naming.
