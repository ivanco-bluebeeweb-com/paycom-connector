# Paycom Connector — Auth and Credentials

## Standard B1-B10 Compliance
- **B1 (Explicit Credentials):** Only accepts explicit `api_token` and `client_code`.
- **B7 (Multi-Tenancy & Scoping):** Mandates `client_code` parameter to enforce strict company boundary separation.
- **B8 (Secret Redaction):** `api_token` is sanitized (`_sanitize_msg`) in all error traces and log messages.
- **B9 (Multi-Account Isolation):** Stored in `paycom_connections` secret vault with active connection selection and connection_id resolution.
- **B10 (Error Classification):** Differentiates HTTP 401, 403, and 429 status codes cleanly.
