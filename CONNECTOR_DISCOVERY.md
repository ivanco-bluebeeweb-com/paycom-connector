# Paycom Connector — Connector Discovery

## Service Overview
Paycom provides cloud-based human capital management software including payroll, time and labor management, talent acquisition, and HR management.

## API Authentication & Multi-Tenancy
- **Authentication Header:** `Authorization: Bearer <api_token>`
- **Client Header:** `X-Client-Code: <client_code>`
- **Multi-Tenancy:** Each connection binds an explicit `api_token` and `client_code` pair to isolate client data across distinct company accounts (Standard B9).

## Rate Limiting & Error Semantics
- HTTP 429: Handled with exponential backoff and `Retry-After` header parsing.
- HTTP 401: Classified as `UNAUTHORIZED` when API token is expired or invalid.
- HTTP 403: Classified as `FORBIDDEN` when client permissions or security restrictions block access.
