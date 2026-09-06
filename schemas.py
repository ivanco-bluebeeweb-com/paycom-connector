"""Pydantic schemas for Paycom Connector (C28. Payroll & Benefits Administration)."""
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameter model."""
    pass

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Acme Paycom.")
    api_token: str = Field(description="Paycom Web Services API Bearer Token.")
    client_code: str = Field(default="", description="Paycom Client Code.")
    base_url: str = Field(default="", description="Optional custom base URL or instance domain.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    base_url: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int

class DeleteResult(BaseModel):
    id: str
    deleted: bool
    message: str

class ListEmployeeParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetEmployeeParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    employee_id: str = Field(description="Unique identifier of the employee.")

class CreateEmployeeParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateEmployeeParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    employee_id: str = Field(description="Unique identifier of the employee.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteEmployeeParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    employee_id: str = Field(description="Unique identifier of the employee.")

class EmployeeRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class EmployeeList(BaseModel):
    items: list[EmployeeRecord]
    total: int
    next_cursor: Optional[str] = None

class ListPayrollRunParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetPayrollRunParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payroll_run_id: str = Field(description="Unique identifier of the payroll_run.")

class CreatePayrollRunParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdatePayrollRunParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payroll_run_id: str = Field(description="Unique identifier of the payroll_run.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeletePayrollRunParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payroll_run_id: str = Field(description="Unique identifier of the payroll_run.")

class PayrollRunRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class PayrollRunList(BaseModel):
    items: list[PayrollRunRecord]
    total: int
    next_cursor: Optional[str] = None

class ListDepartmentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetDepartmentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    department_id: str = Field(description="Unique identifier of the department.")

class CreateDepartmentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateDepartmentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    department_id: str = Field(description="Unique identifier of the department.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteDepartmentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    department_id: str = Field(description="Unique identifier of the department.")

class DepartmentRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class DepartmentList(BaseModel):
    items: list[DepartmentRecord]
    total: int
    next_cursor: Optional[str] = None

class ListTimeOffRequestParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetTimeOffRequestParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    time_off_request_id: str = Field(description="Unique identifier of the time_off_request.")

class CreateTimeOffRequestParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateTimeOffRequestParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    time_off_request_id: str = Field(description="Unique identifier of the time_off_request.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteTimeOffRequestParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    time_off_request_id: str = Field(description="Unique identifier of the time_off_request.")

class TimeOffRequestRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class TimeOffRequestList(BaseModel):
    items: list[TimeOffRequestRecord]
    total: int
    next_cursor: Optional[str] = None

class ListBenefitPlanParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetBenefitPlanParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    benefit_plan_id: str = Field(description="Unique identifier of the benefit_plan.")

class CreateBenefitPlanParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateBenefitPlanParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    benefit_plan_id: str = Field(description="Unique identifier of the benefit_plan.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteBenefitPlanParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    benefit_plan_id: str = Field(description="Unique identifier of the benefit_plan.")

class BenefitPlanRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class BenefitPlanList(BaseModel):
    items: list[BenefitPlanRecord]
    total: int
    next_cursor: Optional[str] = None

class ListDirectDepositParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetDirectDepositParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    direct_deposit_id: str = Field(description="Unique identifier of the direct_deposit.")

class CreateDirectDepositParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateDirectDepositParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    direct_deposit_id: str = Field(description="Unique identifier of the direct_deposit.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteDirectDepositParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    direct_deposit_id: str = Field(description="Unique identifier of the direct_deposit.")

class DirectDepositRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class DirectDepositList(BaseModel):
    items: list[DirectDepositRecord]
    total: int
    next_cursor: Optional[str] = None

class AuditPayrollComplianceResult(BaseModel):
    summary: str
    metrics: dict[str, Any]
    timestamp: str

class GetHeadcountSummaryResult(BaseModel):
    summary: str
    metrics: dict[str, Any]
    timestamp: str
