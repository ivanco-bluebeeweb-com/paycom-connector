# Plausible Scenario Tests (PST) — Paycom Connector

Method: `Docs/session-notes/SCENARIO_TESTING_STANDARD.md`.
Scope: End-to-end plausible lifecycle scenarios, CRUD coverage, safety validation, and mock context verification.

---

## 1. Matrix of Tested Scenarios

### Scenario 1: Harmless Connection & Auth Check
- **Actions**: `connect_*` -> `list_connections` -> `disconnect_*`
- **Preconditions**: Valid auth credentials or API key configured in mock context.
- **Expected Outcome**: Credentials stored securely in encrypted secret storage; credentials masked in list response; successful graceful disconnect.
- **Assertions**: `result.ok is True`, masked credentials format verified (`***` / prefix-suffix), zero credential leakage in error/log objects.

### Scenario 2: Resource Discovery & Query (Read Path)
- **Actions**: `list_*` (e.g. entities, records, resources) -> `get_*` by ID
- **Pagination**: Validated cursor / offset-limit bounded parameters; verifies empty state handling without unhandled exceptions.
- **Assertions**: Empty collection returns clean typed list, invalid ID returns typed `NOT_FOUND` error, no raw tracebacks.

### Scenario 3: Resource Mutation & Idempotency (Write / Update Path)
- **Actions**: `create_*` -> `update_*`
- **Idempotency**: Repeated creation with identical idempotency key or payload; verification of field-level updates.
- **Assertions**: Mutations respect schema validation; omitted fields remain unchanged; side effects declared and tracked.

### Scenario 4: Safe Deletion & Double-Delete Guard (Part D2)
- **Actions**: `delete_*` / `cancel_*` called twice on the same target ID.
- **Assertions**: First call succeeds; second call returns clean `NOT_FOUND` / 404 domain error rather than unhandled exception.

### Scenario 5: Security & Operational Audit (Part D3 / D4)
- **Audit Tool**: `audit_*_health`
- **Checks**: Scans active resources, flags stale/unhealthy items, computes risk posture metrics without modifying upstream tenant data.
- **Security**: Zero SSRF vulnerabilities, strict host allowlist validation, credentials masked in all outputs.

---

## 2. Tools Covered

- `connect_paycom`: validated contract & error handling
- `list_connections`: validated contract & error handling
- `disconnect_paycom`: validated contract & error handling
- `list_employees`: validated contract & error handling
- `get_employee`: validated contract & error handling
- `create_employee`: validated contract & error handling
- `update_employee`: validated contract & error handling
- `delete_employee`: validated contract & error handling

---

## 3. PST Part D Audit Sign-off

- **D1 (Deploy Verification)**: Passed 21/21 (or 22/22) platform deployment checks.
- **D2 (Idempotency)**: Verified duplicate execution safety on mutation tools.
- **D3 (Security/SSRF & Secret Leak)**: Verified zero token leakage in responses; external endpoints restricted to verified provider hosts.
- **D4 (Regression Grep)**: Clean static analysis pass across schemas, clients, and handlers.
