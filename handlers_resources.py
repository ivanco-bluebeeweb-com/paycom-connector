"""Resource handlers for Paycom Connector."""
from __future__ import annotations
from app import chat
import datetime
from imperal_sdk import ActionResult
from paycom_client import PaycomClient
from handlers_connection import resolve_connection
from schemas import *

async def _get_client(ctx, cid: str = ""):
    conn = await resolve_connection(ctx, cid)
    if not conn:
        return None, ActionResult.error("No active Paycom connection", code="UNAUTHORIZED")
    return PaycomClient(api_token=conn["api_token"], base_url=conn.get("base_url", "")), None

@chat.function(
    "list_employees",
    "List employees (Worker identity, employment details and compensation).",
    action_type="read",
    chain_callable=True,
    data_model=ListEmployeeParams
)
@chat.function(
    "list_employees",
    "List employees (Worker identity, employment details and compensation).",
    action_type="read",
    chain_callable=True,
    data_model=ListEmployeeParams
)
async def list_employees(ctx, params: ListEmployeeParams) -> ActionResult[EmployeeList]:
    """Execute list employees operation."""
    """Execute list employees operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_employees(limit=params.limit, cursor=params.cursor)
    items = [EmployeeRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(EmployeeList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_employee",
    "Read details of one employee.",
    action_type="read",
    chain_callable=True,
    data_model=GetEmployeeParams
)
@chat.function(
    "get_employee",
    "Read details of one employee.",
    action_type="read",
    chain_callable=True,
    data_model=GetEmployeeParams
)
async def get_employee(ctx, params: GetEmployeeParams) -> ActionResult[EmployeeRecord]:
    """Execute get employee operation."""
    """Execute get employee operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_employee(params.employee_id)
    return ActionResult.ok(EmployeeRecord(id=str(data.get("id", params.employee_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_employee",
    "Create a new employee.",
    action_type="read",
    chain_callable=True,
    data_model=CreateEmployeeParams
)
@chat.function(
    "create_employee",
    "Create a new employee.",
    action_type="read",
    chain_callable=True,
    data_model=CreateEmployeeParams
)
async def create_employee(ctx, params: CreateEmployeeParams) -> ActionResult[EmployeeRecord]:
    """Execute create employee operation."""
    """Execute create employee operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_employee(name=params.name, details=params.details)
    return ActionResult.ok(EmployeeRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_employee",
    "Update an existing employee.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateEmployeeParams
)
@chat.function(
    "update_employee",
    "Update an existing employee.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateEmployeeParams
)
async def update_employee(ctx, params: UpdateEmployeeParams) -> ActionResult[EmployeeRecord]:
    """Execute update employee operation."""
    """Execute update employee operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_employee(params.employee_id, params.fields)
    return ActionResult.ok(EmployeeRecord(id=params.employee_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_employee",
    "Permanently delete a employee.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteEmployeeParams
)
@chat.function(
    "delete_employee",
    "Permanently delete a employee.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteEmployeeParams
)
async def delete_employee(ctx, params: DeleteEmployeeParams) -> ActionResult[DeleteResult]:
    """Execute delete employee operation."""
    """Execute delete employee operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_employee(params.employee_id)
    return ActionResult.ok(DeleteResult(id=params.employee_id, deleted=ok, message="employee deleted"))

@chat.function(
    "list_payroll_runs",
    "List payroll_runs (Executed or scheduled payroll cycle batch).",
    action_type="read",
    chain_callable=True,
    data_model=ListPayrollRunParams
)
@chat.function(
    "list_payroll_runs",
    "List payroll_runs (Executed or scheduled payroll cycle batch).",
    action_type="read",
    chain_callable=True,
    data_model=ListPayrollRunParams
)
async def list_payroll_runs(ctx, params: ListPayrollRunParams) -> ActionResult[PayrollRunList]:
    """Execute list payroll runs operation."""
    """Execute list payroll runs operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_payroll_runs(limit=params.limit, cursor=params.cursor)
    items = [PayrollRunRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(PayrollRunList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_payroll_run",
    "Read details of one payroll_run.",
    action_type="read",
    chain_callable=True,
    data_model=GetPayrollRunParams
)
@chat.function(
    "get_payroll_run",
    "Read details of one payroll_run.",
    action_type="read",
    chain_callable=True,
    data_model=GetPayrollRunParams
)
async def get_payroll_run(ctx, params: GetPayrollRunParams) -> ActionResult[PayrollRunRecord]:
    """Execute get payroll run operation."""
    """Execute get payroll run operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_payroll_run(params.payroll_run_id)
    return ActionResult.ok(PayrollRunRecord(id=str(data.get("id", params.payroll_run_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_payroll_run",
    "Create a new payroll_run.",
    action_type="read",
    chain_callable=True,
    data_model=CreatePayrollRunParams
)
@chat.function(
    "create_payroll_run",
    "Create a new payroll_run.",
    action_type="read",
    chain_callable=True,
    data_model=CreatePayrollRunParams
)
async def create_payroll_run(ctx, params: CreatePayrollRunParams) -> ActionResult[PayrollRunRecord]:
    """Execute create payroll run operation."""
    """Execute create payroll run operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_payroll_run(name=params.name, details=params.details)
    return ActionResult.ok(PayrollRunRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_payroll_run",
    "Update an existing payroll_run.",
    action_type="read",
    chain_callable=True,
    data_model=UpdatePayrollRunParams
)
@chat.function(
    "update_payroll_run",
    "Update an existing payroll_run.",
    action_type="read",
    chain_callable=True,
    data_model=UpdatePayrollRunParams
)
async def update_payroll_run(ctx, params: UpdatePayrollRunParams) -> ActionResult[PayrollRunRecord]:
    """Execute update payroll run operation."""
    """Execute update payroll run operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_payroll_run(params.payroll_run_id, params.fields)
    return ActionResult.ok(PayrollRunRecord(id=params.payroll_run_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_payroll_run",
    "Permanently delete a payroll_run.",
    action_type="read",
    chain_callable=True,
    data_model=DeletePayrollRunParams
)
@chat.function(
    "delete_payroll_run",
    "Permanently delete a payroll_run.",
    action_type="read",
    chain_callable=True,
    data_model=DeletePayrollRunParams
)
async def delete_payroll_run(ctx, params: DeletePayrollRunParams) -> ActionResult[DeleteResult]:
    """Execute delete payroll run operation."""
    """Execute delete payroll run operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_payroll_run(params.payroll_run_id)
    return ActionResult.ok(DeleteResult(id=params.payroll_run_id, deleted=ok, message="payroll_run deleted"))

@chat.function(
    "list_departments",
    "List departments (Organizational department and cost center).",
    action_type="read",
    chain_callable=True,
    data_model=ListDepartmentParams
)
@chat.function(
    "list_departments",
    "List departments (Organizational department and cost center).",
    action_type="read",
    chain_callable=True,
    data_model=ListDepartmentParams
)
async def list_departments(ctx, params: ListDepartmentParams) -> ActionResult[DepartmentList]:
    """Execute list departments operation."""
    """Execute list departments operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_departments(limit=params.limit, cursor=params.cursor)
    items = [DepartmentRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(DepartmentList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_department",
    "Read details of one department.",
    action_type="read",
    chain_callable=True,
    data_model=GetDepartmentParams
)
@chat.function(
    "get_department",
    "Read details of one department.",
    action_type="read",
    chain_callable=True,
    data_model=GetDepartmentParams
)
async def get_department(ctx, params: GetDepartmentParams) -> ActionResult[DepartmentRecord]:
    """Execute get department operation."""
    """Execute get department operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_department(params.department_id)
    return ActionResult.ok(DepartmentRecord(id=str(data.get("id", params.department_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_department",
    "Create a new department.",
    action_type="read",
    chain_callable=True,
    data_model=CreateDepartmentParams
)
@chat.function(
    "create_department",
    "Create a new department.",
    action_type="read",
    chain_callable=True,
    data_model=CreateDepartmentParams
)
async def create_department(ctx, params: CreateDepartmentParams) -> ActionResult[DepartmentRecord]:
    """Execute create department operation."""
    """Execute create department operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_department(name=params.name, details=params.details)
    return ActionResult.ok(DepartmentRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_department",
    "Update an existing department.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateDepartmentParams
)
@chat.function(
    "update_department",
    "Update an existing department.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateDepartmentParams
)
async def update_department(ctx, params: UpdateDepartmentParams) -> ActionResult[DepartmentRecord]:
    """Execute update department operation."""
    """Execute update department operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_department(params.department_id, params.fields)
    return ActionResult.ok(DepartmentRecord(id=params.department_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_department",
    "Permanently delete a department.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteDepartmentParams
)
@chat.function(
    "delete_department",
    "Permanently delete a department.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteDepartmentParams
)
async def delete_department(ctx, params: DeleteDepartmentParams) -> ActionResult[DeleteResult]:
    """Execute delete department operation."""
    """Execute delete department operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_department(params.department_id)
    return ActionResult.ok(DeleteResult(id=params.department_id, deleted=ok, message="department deleted"))

@chat.function(
    "list_time_off_requests",
    "List time_off_requests (Leave and PTO balance request).",
    action_type="read",
    chain_callable=True,
    data_model=ListTimeOffRequestParams
)
@chat.function(
    "list_time_off_requests",
    "List time_off_requests (Leave and PTO balance request).",
    action_type="read",
    chain_callable=True,
    data_model=ListTimeOffRequestParams
)
async def list_time_off_requests(ctx, params: ListTimeOffRequestParams) -> ActionResult[TimeOffRequestList]:
    """Execute list time off requests operation."""
    """Execute list time off requests operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_time_off_requests(limit=params.limit, cursor=params.cursor)
    items = [TimeOffRequestRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(TimeOffRequestList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_time_off_request",
    "Read details of one time_off_request.",
    action_type="read",
    chain_callable=True,
    data_model=GetTimeOffRequestParams
)
@chat.function(
    "get_time_off_request",
    "Read details of one time_off_request.",
    action_type="read",
    chain_callable=True,
    data_model=GetTimeOffRequestParams
)
async def get_time_off_request(ctx, params: GetTimeOffRequestParams) -> ActionResult[TimeOffRequestRecord]:
    """Execute get time off request operation."""
    """Execute get time off request operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_time_off_request(params.time_off_request_id)
    return ActionResult.ok(TimeOffRequestRecord(id=str(data.get("id", params.time_off_request_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_time_off_request",
    "Create a new time_off_request.",
    action_type="read",
    chain_callable=True,
    data_model=CreateTimeOffRequestParams
)
@chat.function(
    "create_time_off_request",
    "Create a new time_off_request.",
    action_type="read",
    chain_callable=True,
    data_model=CreateTimeOffRequestParams
)
async def create_time_off_request(ctx, params: CreateTimeOffRequestParams) -> ActionResult[TimeOffRequestRecord]:
    """Execute create time off request operation."""
    """Execute create time off request operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_time_off_request(name=params.name, details=params.details)
    return ActionResult.ok(TimeOffRequestRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_time_off_request",
    "Update an existing time_off_request.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateTimeOffRequestParams
)
@chat.function(
    "update_time_off_request",
    "Update an existing time_off_request.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateTimeOffRequestParams
)
async def update_time_off_request(ctx, params: UpdateTimeOffRequestParams) -> ActionResult[TimeOffRequestRecord]:
    """Execute update time off request operation."""
    """Execute update time off request operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_time_off_request(params.time_off_request_id, params.fields)
    return ActionResult.ok(TimeOffRequestRecord(id=params.time_off_request_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_time_off_request",
    "Permanently delete a time_off_request.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteTimeOffRequestParams
)
@chat.function(
    "delete_time_off_request",
    "Permanently delete a time_off_request.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteTimeOffRequestParams
)
async def delete_time_off_request(ctx, params: DeleteTimeOffRequestParams) -> ActionResult[DeleteResult]:
    """Execute delete time off request operation."""
    """Execute delete time off request operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_time_off_request(params.time_off_request_id)
    return ActionResult.ok(DeleteResult(id=params.time_off_request_id, deleted=ok, message="time_off_request deleted"))

@chat.function(
    "list_benefit_plans",
    "List benefit_plans (Company healthcare and benefits package).",
    action_type="read",
    chain_callable=True,
    data_model=ListBenefitPlanParams
)
@chat.function(
    "list_benefit_plans",
    "List benefit_plans (Company healthcare and benefits package).",
    action_type="read",
    chain_callable=True,
    data_model=ListBenefitPlanParams
)
async def list_benefit_plans(ctx, params: ListBenefitPlanParams) -> ActionResult[BenefitPlanList]:
    """Execute list benefit plans operation."""
    """Execute list benefit plans operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_benefit_plans(limit=params.limit, cursor=params.cursor)
    items = [BenefitPlanRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(BenefitPlanList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_benefit_plan",
    "Read details of one benefit_plan.",
    action_type="read",
    chain_callable=True,
    data_model=GetBenefitPlanParams
)
@chat.function(
    "get_benefit_plan",
    "Read details of one benefit_plan.",
    action_type="read",
    chain_callable=True,
    data_model=GetBenefitPlanParams
)
async def get_benefit_plan(ctx, params: GetBenefitPlanParams) -> ActionResult[BenefitPlanRecord]:
    """Execute get benefit plan operation."""
    """Execute get benefit plan operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_benefit_plan(params.benefit_plan_id)
    return ActionResult.ok(BenefitPlanRecord(id=str(data.get("id", params.benefit_plan_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_benefit_plan",
    "Create a new benefit_plan.",
    action_type="read",
    chain_callable=True,
    data_model=CreateBenefitPlanParams
)
@chat.function(
    "create_benefit_plan",
    "Create a new benefit_plan.",
    action_type="read",
    chain_callable=True,
    data_model=CreateBenefitPlanParams
)
async def create_benefit_plan(ctx, params: CreateBenefitPlanParams) -> ActionResult[BenefitPlanRecord]:
    """Execute create benefit plan operation."""
    """Execute create benefit plan operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_benefit_plan(name=params.name, details=params.details)
    return ActionResult.ok(BenefitPlanRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_benefit_plan",
    "Update an existing benefit_plan.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateBenefitPlanParams
)
@chat.function(
    "update_benefit_plan",
    "Update an existing benefit_plan.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateBenefitPlanParams
)
async def update_benefit_plan(ctx, params: UpdateBenefitPlanParams) -> ActionResult[BenefitPlanRecord]:
    """Execute update benefit plan operation."""
    """Execute update benefit plan operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_benefit_plan(params.benefit_plan_id, params.fields)
    return ActionResult.ok(BenefitPlanRecord(id=params.benefit_plan_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_benefit_plan",
    "Permanently delete a benefit_plan.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteBenefitPlanParams
)
@chat.function(
    "delete_benefit_plan",
    "Permanently delete a benefit_plan.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteBenefitPlanParams
)
async def delete_benefit_plan(ctx, params: DeleteBenefitPlanParams) -> ActionResult[DeleteResult]:
    """Execute delete benefit plan operation."""
    """Execute delete benefit plan operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_benefit_plan(params.benefit_plan_id)
    return ActionResult.ok(DeleteResult(id=params.benefit_plan_id, deleted=ok, message="benefit_plan deleted"))

@chat.function(
    "list_direct_deposits",
    "List direct_deposits (Employee bank routing disbursement setting).",
    action_type="read",
    chain_callable=True,
    data_model=ListDirectDepositParams
)
@chat.function(
    "list_direct_deposits",
    "List direct_deposits (Employee bank routing disbursement setting).",
    action_type="read",
    chain_callable=True,
    data_model=ListDirectDepositParams
)
async def list_direct_deposits(ctx, params: ListDirectDepositParams) -> ActionResult[DirectDepositList]:
    """Execute list direct deposits operation."""
    """Execute list direct deposits operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_direct_deposits(limit=params.limit, cursor=params.cursor)
    items = [DirectDepositRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(DirectDepositList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_direct_deposit",
    "Read details of one direct_deposit.",
    action_type="read",
    chain_callable=True,
    data_model=GetDirectDepositParams
)
@chat.function(
    "get_direct_deposit",
    "Read details of one direct_deposit.",
    action_type="read",
    chain_callable=True,
    data_model=GetDirectDepositParams
)
async def get_direct_deposit(ctx, params: GetDirectDepositParams) -> ActionResult[DirectDepositRecord]:
    """Execute get direct deposit operation."""
    """Execute get direct deposit operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_direct_deposit(params.direct_deposit_id)
    return ActionResult.ok(DirectDepositRecord(id=str(data.get("id", params.direct_deposit_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_direct_deposit",
    "Create a new direct_deposit.",
    action_type="read",
    chain_callable=True,
    data_model=CreateDirectDepositParams
)
@chat.function(
    "create_direct_deposit",
    "Create a new direct_deposit.",
    action_type="read",
    chain_callable=True,
    data_model=CreateDirectDepositParams
)
async def create_direct_deposit(ctx, params: CreateDirectDepositParams) -> ActionResult[DirectDepositRecord]:
    """Execute create direct deposit operation."""
    """Execute create direct deposit operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_direct_deposit(name=params.name, details=params.details)
    return ActionResult.ok(DirectDepositRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_direct_deposit",
    "Update an existing direct_deposit.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateDirectDepositParams
)
@chat.function(
    "update_direct_deposit",
    "Update an existing direct_deposit.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateDirectDepositParams
)
async def update_direct_deposit(ctx, params: UpdateDirectDepositParams) -> ActionResult[DirectDepositRecord]:
    """Execute update direct deposit operation."""
    """Execute update direct deposit operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_direct_deposit(params.direct_deposit_id, params.fields)
    return ActionResult.ok(DirectDepositRecord(id=params.direct_deposit_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_direct_deposit",
    "Permanently delete a direct_deposit.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteDirectDepositParams
)
@chat.function(
    "delete_direct_deposit",
    "Permanently delete a direct_deposit.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteDirectDepositParams
)
async def delete_direct_deposit(ctx, params: DeleteDirectDepositParams) -> ActionResult[DeleteResult]:
    """Execute delete direct deposit operation."""
    """Execute delete direct deposit operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_direct_deposit(params.direct_deposit_id)
    return ActionResult.ok(DeleteResult(id=params.direct_deposit_id, deleted=ok, message="direct_deposit deleted"))

@chat.function(
    "audit_payroll_compliance",
    "Value-add audit: Audit worker onboarding completeness, tax filings and missing info.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionIdParams
)
@chat.function(
    "audit_payroll_compliance",
    "Value-add audit: Audit worker onboarding completeness, tax filings and missing info.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionIdParams
)
async def audit_payroll_compliance(ctx, params: ConnectionIdParams) -> ActionResult[AuditPayrollComplianceResult]:
    """Execute audit payroll compliance operation."""
    """Execute audit payroll compliance operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.ok(AuditPayrollComplianceResult(
        summary="Paycom Audit worker onboarding completeness, tax filings and missing info",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ))

@chat.function(
    "get_headcount_summary",
    "Value-add audit: Summary of active headcount by department and location.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionIdParams
)
@chat.function(
    "get_headcount_summary",
    "Value-add audit: Summary of active headcount by department and location.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionIdParams
)
async def get_headcount_summary(ctx, params: ConnectionIdParams) -> ActionResult[GetHeadcountSummaryResult]:
    """Execute get headcount summary operation."""
    """Execute get headcount summary operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.ok(GetHeadcountSummaryResult(
        summary="Paycom Summary of active headcount by department and location",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ))
