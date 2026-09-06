"""Official Paycom REST API client with client_code scoping and sanitized error handling."""
from __future__ import annotations
import httpx
from typing import Any, Optional

DEFAULT_PAYCOM_BASE = "https://api.paycom.com"

class PaycomClient:
    def __init__(self, api_token: str, client_code: str = "", base_url: str = ""):
        self.api_token = api_token.strip()
        self.client_code = str(client_code).strip()
        self.base_url = (base_url.strip() if base_url else DEFAULT_PAYCOM_BASE).rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Imperal-Paycom/0.1.0"
        }
        if self.client_code:
            self.headers["X-Client-Code"] = self.client_code
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    def _sanitize_msg(self, msg: str) -> str:
        if not msg:
            return ""
        if self.api_token and len(self.api_token) > 6:
            msg = msg.replace(self.api_token, self.api_token[:3] + "..." + self.api_token[-3:])
        return msg

    def _classify_error(self, resp: httpx.Response, action_name: str) -> dict[str, Any]:
        status = resp.status_code
        err_msg = ""
        try:
            data = resp.json()
            if "errors" in data and isinstance(data["errors"], list) and len(data["errors"]) > 0:
                err_msg = "; ".join(e.get("message", "") for e in data["errors"])
            elif "message" in data:
                err_msg = data["message"]
            elif "error" in data:
                err_msg = str(data["error"])
        except Exception:
            err_msg = resp.text[:200]
        err_msg = self._sanitize_msg(err_msg)

        if status == 429:
            retry_after = resp.headers.get("Retry-After", "60")
            return {
                "status": "error",
                "code": "RATE_LIMITED",
                "message": f"Paycom rate limit reached during {action_name}. Retry after {retry_after}s.",
                "retry_after": int(retry_after) if retry_after.isdigit() else 60
            }
        elif status == 401:
            return {"status": "error", "code": "UNAUTHORIZED", "message": f"Unauthorized Paycom request during {action_name}: {err_msg or 'Invalid API token or client credentials.'}"}
        elif status == 403:
            return {"status": "error", "code": "FORBIDDEN", "message": f"Access forbidden in Paycom for {action_name}: {err_msg or 'Insufficient permissions or invalid client code.'}"}
        elif status == 404:
            return {"status": "error", "code": "NOT_FOUND", "message": f"Paycom resource not found in {action_name}: {err_msg}"}
        return {"status": "error", "code": f"HTTP_{status}", "message": f"Paycom API returned status {status} during {action_name}: {err_msg}"}

    async def verify_auth(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/api/v1/auth/verify", headers=self.headers)
                if resp.status_code in (200, 201):
                    return {"status": "connected", "verified": True, "data": resp.json()}
                if resp.status_code in (401, 403, 429):
                    return self._classify_error(resp, "verify_auth")
                return {"status": "connected", "verified": True}
            except Exception as e:
                return {"status": "error", "code": "CONNECTION_FAILED", "message": self._sanitize_msg(str(e))}

    async def list_employees(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = {"limit": limit}
                if cursor: params["cursor"] = cursor
                resp = await client.get(f"{self.base_url}/api/v1/employees", headers=self.headers, params=params)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    items = data if isinstance(data, list) else data.get("employees", [])
                    return {"items": items, "total": len(items)}
                return self._classify_error(resp, "list_employees")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def get_employee(self, employee_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/api/v1/employees/{employee_id}", headers=self.headers)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "get_employee")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def create_employee(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/api/v1/employees", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_employee")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def update_employee(self, employee_id: str, details: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/api/v1/employees/{employee_id}", headers=self.headers, json=details)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "update_employee")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def delete_employee(self, employee_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/api/v1/employees/{employee_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": employee_id, "deleted": True, "message": "Employee deleted"}
                return self._classify_error(resp, "delete_employee")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def list_payroll_runs(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = {"limit": limit}
                if cursor: params["cursor"] = cursor
                resp = await client.get(f"{self.base_url}/api/v1/payroll/runs", headers=self.headers, params=params)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    items = data if isinstance(data, list) else data.get("payroll_runs", [])
                    return {"items": items, "total": len(items)}
                return self._classify_error(resp, "list_payroll_runs")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def get_payroll_run(self, run_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/api/v1/payroll/runs/{run_id}", headers=self.headers)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "get_payroll_run")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def create_payroll_run(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/api/v1/payroll/runs", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_payroll_run")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def update_payroll_run(self, run_id: str, details: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/api/v1/payroll/runs/{run_id}", headers=self.headers, json=details)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "update_payroll_run")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def delete_payroll_run(self, run_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/api/v1/payroll/runs/{run_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": run_id, "deleted": True, "message": "Payroll run deleted"}
                return self._classify_error(resp, "delete_payroll_run")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def list_departments(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = {"limit": limit}
                if cursor: params["cursor"] = cursor
                resp = await client.get(f"{self.base_url}/api/v1/departments", headers=self.headers, params=params)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    items = data if isinstance(data, list) else data.get("departments", [])
                    return {"items": items, "total": len(items)}
                return self._classify_error(resp, "list_departments")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def get_department(self, dept_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/api/v1/departments/{dept_id}", headers=self.headers)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "get_department")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def create_department(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/api/v1/departments", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_department")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def update_department(self, dept_id: str, details: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/api/v1/departments/{dept_id}", headers=self.headers, json=details)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "update_department")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def delete_department(self, dept_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/api/v1/departments/{dept_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": dept_id, "deleted": True, "message": "Department deleted"}
                return self._classify_error(resp, "delete_department")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def list_time_off_requests(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = {"limit": limit}
                if cursor: params["cursor"] = cursor
                resp = await client.get(f"{self.base_url}/api/v1/timeoff", headers=self.headers, params=params)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    items = data if isinstance(data, list) else data.get("time_off_requests", [])
                    return {"items": items, "total": len(items)}
                return self._classify_error(resp, "list_time_off_requests")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def get_time_off_request(self, req_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/api/v1/timeoff/{req_id}", headers=self.headers)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "get_time_off_request")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def create_time_off_request(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/api/v1/timeoff", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_time_off_request")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def update_time_off_request(self, req_id: str, details: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/api/v1/timeoff/{req_id}", headers=self.headers, json=details)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "update_time_off_request")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def delete_time_off_request(self, req_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/api/v1/timeoff/{req_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": req_id, "deleted": True, "message": "Time-off request deleted"}
                return self._classify_error(resp, "delete_time_off_request")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def list_benefit_plans(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = {"limit": limit}
                if cursor: params["cursor"] = cursor
                resp = await client.get(f"{self.base_url}/api/v1/benefits", headers=self.headers, params=params)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    items = data if isinstance(data, list) else data.get("benefit_plans", [])
                    return {"items": items, "total": len(items)}
                return self._classify_error(resp, "list_benefit_plans")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def get_benefit_plan(self, plan_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/api/v1/benefits/{plan_id}", headers=self.headers)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "get_benefit_plan")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def create_benefit_plan(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/api/v1/benefits", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_benefit_plan")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def update_benefit_plan(self, plan_id: str, details: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/api/v1/benefits/{plan_id}", headers=self.headers, json=details)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "update_benefit_plan")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def delete_benefit_plan(self, plan_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/api/v1/benefits/{plan_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": plan_id, "deleted": True, "message": "Benefit plan deleted"}
                return self._classify_error(resp, "delete_benefit_plan")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def list_direct_deposits(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = {"limit": limit}
                if cursor: params["cursor"] = cursor
                resp = await client.get(f"{self.base_url}/api/v1/directdeposits", headers=self.headers, params=params)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    items = data if isinstance(data, list) else data.get("direct_deposits", [])
                    return {"items": items, "total": len(items)}
                return self._classify_error(resp, "list_direct_deposits")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def get_direct_deposit(self, dd_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/api/v1/directdeposits/{dd_id}", headers=self.headers)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "get_direct_deposit")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def create_direct_deposit(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/api/v1/directdeposits", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_direct_deposit")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def update_direct_deposit(self, dd_id: str, details: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/api/v1/directdeposits/{dd_id}", headers=self.headers, json=details)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "update_direct_deposit")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}

    async def delete_direct_deposit(self, dd_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/api/v1/directdeposits/{dd_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": dd_id, "deleted": True, "message": "Direct deposit deleted"}
                return self._classify_error(resp, "delete_direct_deposit")
            except Exception as e:
                return {"status": "error", "code": "REQUEST_FAILED", "message": self._sanitize_msg(str(e))}
