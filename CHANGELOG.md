# Changelog

## v0.1.2 - 2026-03-01

Patch release based on `main`, focused on containerized operations, runtime path
resolution hardening, and post-release usability/documentation improvements.

### Added

- Container-first deployment assets and CI workflow updates:
  - runtime/test Docker targets
  - compose profiles and production preflight checks
  - GHCR build/publish automation refinements
- `gcc-cli scaffold skill` support for `codex` and `generic` templates.
- Host-to-runtime path translation controls:
  - `GCC_MCP_PATH_MAP`
  - `GCC_MCP_ALLOWED_ROOTS`
- Timeout diagnostics with request correlation metadata and phase-level logging.

### Changed

- Directory resolution now reports both requested and resolved path contract fields in
  error details, while preserving backward-compatible metadata keys.
- Mapped directory handling now includes bounded ancestor fallback and clearer relative-path guidance.
- Onboarding and installation documentation now explicitly distinguishes local vs container path behavior.

### Fixed

- MCP discoverability guidance now clarifies that an empty resources list does not imply
  unavailable tools; troubleshooting now includes direct tool ping validation.
- Context tag-filter semantics after merges are documented and regression-tested:
  `scope=[\"main\"]` only returns entries with tags present on `main` history entries.

## v0.1.1 - 2026-02-20

First public release of `gcc-mcp`, including the complete implementation history delivered from
initial scaffold through production-readiness and automated release publishing.

### Added

- Core MCP tool surface:
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
- CLI parity commands (`gcc-cli`) for all major MCP operations, including audit verification.
- Streamable HTTP transport mode (stdio remains default) with runtime-configurable host/port.
- Remote auth modes for HTTP transport:
  - `token`
  - `trusted-proxy-header`
  - `oauth2` introspection
- Runtime security profile system:
  - `baseline`
  - `strict` (auth/audit/signing enforced for remote operation)
- Signed audit logging with HMAC hash-chain metadata.
- Audit verification command:
  - `gcc-cli audit-verify`
  - rotated key support via keyring file
- Operational controls:
  - per-process rate limit (`rate-limit-per-minute`)
  - audit field truncation control (`audit-max-field-chars`)
- Production CI gates:
  - lint/test/compile matrix
  - security scanning (`bandit`, `pip-audit`)
  - package gate (`python -m build`, `twine check`, wheel install smoke)
- Runtime startup preflight diagnostics:
  - `gcc-mcp --check-config`
  - `gcc-mcp --print-effective-config` (sanitized output)
- Automated release workflow:
  - merged `release:` PR to `main` auto-publishes tag/release
  - release metadata sourced from `pyproject.toml` + `CHANGELOG.md`
  - workflow-dispatch fallback for backfill releases

### Improved

- FastMCP compatibility hardening across SDK drift:
  - constructor compatibility fallback behavior
  - tool-registration fallback robustness for older SDK annotation behavior
  - regression coverage for compatibility paths and error propagation
- CI matrix coverage for MCP SDK compatibility (default + minimum supported version).
- Changelog-backed release notes quality and deterministic release publication.
- Project tracking and phase closeout documentation through v1.6 planning.

### Security

- Reinforced remote-deployment guidance around strict profile, auth mode requirements, and
  signed audit configuration.
- Maintained CI security scans (`bandit`, `pip-audit`) with passing gates on merged delivery.

### Delivery Timeline Included In This First Release

- v0.1: core server, engine model, filesystem persistence, base MCP tools.
- v0.2-v0.3: CLI parity, path hardening, validation and documentation hardening.
- v0.4-v0.6: remote transport hardening, structured auditing, authn/authz framework.
- v0.7-v0.9: strict security policy, signed audit trails, verification, key rotation support.
- v1.0: complete MCP tool surface parity.
- v1.1-v1.3: FastMCP compatibility resilience and CI SDK matrix hardening.
- v1.4: production-readiness checklist and package distribution smoke gates.
- v1.5: startup preflight diagnostics for safe deployment checks.
- v1.6: release automation pipeline for tag/release publication.
