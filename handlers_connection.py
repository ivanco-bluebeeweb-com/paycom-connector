"""Connection lifecycle for Paycom Connector."""
from __future__ import annotations
import json, uuid
from imperal_sdk import ActionResult
from paycom_client import PaycomClient
from app import chat
from schemas import (
    NoParams,
    ConnectParams, ConnectionIdParams, ConnectionList, ConnectionRecord, DeleteResult
)

_SECRET = "paycom_connections"

def _mask(value: str) -> str:
    return value[:4] + "…" + value[-4:] if len(value) > 10 else "***"

async def _load_connections(ctx) -> list[dict]:
    raw = await ctx.secrets.get(_SECRET)
    if not raw: return []
    try: data = json.loads(raw)
    except: return []
    return data if isinstance(data, list) else []

async def _save_connections(ctx, conns: list[dict]) -> None:
    await ctx.secrets.set(_SECRET, json.dumps(conns))

async def resolve_connection(ctx, connection_id: str = "") -> dict | None:
    conns = await _load_connections(ctx)
    if not conns: return None
    if not connection_id:
        for c in conns:
            if c.get("is_active"):
                return c
        return conns[0]
    for c in conns:
        if c["id"] == connection_id:
            return c
    return None

@chat.function(
    "connect_paycom",
    "Connect your own Paycom account with API Token and Client Code.",
    action_type="write",
    chain_callable=True,
    event="paycom-connector.connect_paycom",
    effects=["create:connection"],
    data_model=ConnectParams
)
async def connect_paycom(ctx, params: ConnectParams) -> ActionResult[ConnectionRecord]:
    """Connect a new Paycom client."""
    client = PaycomClient(
        api_token=params.api_token,
        client_code=params.client_code,
        base_url=params.base_url
    )
    v_res = await client.verify_auth()
    if v_res.get("status") == "error":
        return ActionResult.error(
            f"Failed to verify Paycom credentials: {v_res.get('message', 'Unknown error')}",
            code=v_res.get("code", "UNAUTHORIZED")
        )

    conns = await _load_connections(ctx)
    conn_id = f"conn_{uuid.uuid4().hex[:8]}"
    for c in conns:
        c["is_active"] = False

    rec = {
        "id": conn_id,
        "label": params.label.strip() or f"Paycom ({params.client_code or 'Default'})",
        "masked_key": _mask(params.api_token),
        "api_token": params.api_token,
        "client_code": params.client_code,
        "base_url": params.base_url.strip(),
        "is_active": True
    }
    conns.append(rec)
    await _save_connections(ctx, conns)
    return ActionResult.success(
        ConnectionRecord(
            id=rec["id"],
            label=rec["label"],
            masked_key=rec["masked_key"],
            client_code=rec["client_code"],
            base_url=rec["base_url"],
            is_active=rec["is_active"]
        ),
        summary="Paycom connected."
    )

@chat.function(
    "list_connections",
    "List connected Paycom accounts without exposing sensitive tokens.",
    action_type="read",
    chain_callable=True,
    event="paycom-connector.list_connections",
    effects=[],
    data_model=NoParams
)
async def list_connections(ctx, params: NoParams) -> ActionResult[ConnectionList]:
    """List all configured Paycom connections."""
    conns = await _load_connections(ctx)
    records = [
        ConnectionRecord(
            id=c["id"],
            label=c.get("label", ""),
            masked_key=c.get("masked_key", "***"),
            client_code=c.get("client_code", ""),
            base_url=c.get("base_url", ""),
            is_active=c.get("is_active", False)
        )
        for c in conns
    ]
    return ActionResult.success(ConnectionList(connections=records, total=len(records)), summary="Connections listed.")

@chat.function(
    "disconnect_paycom",
    "Disconnect a Paycom account and delete its saved credentials.",
    action_type="write",
    chain_callable=True,
    event="paycom-connector.disconnect_paycom",
    effects=["delete:connection"],
    data_model=ConnectionIdParams
)
async def disconnect_paycom(ctx, params: ConnectionIdParams) -> ActionResult[DeleteResult]:
    """Disconnect a Paycom account."""
    conns = await _load_connections(ctx)
    target = params.connection_id.strip()
    if not target:
        if conns:
            target = conns[0]["id"]
        else:
            return ActionResult.error("No active Paycom connection to disconnect.", code="NOT_FOUND")

    remaining = [c for c in conns if c["id"] != target]
    if len(remaining) == len(conns):
        return ActionResult.error(f"Connection {target} not found.", code="NOT_FOUND")

    if remaining and not any(c.get("is_active") for c in remaining):
        remaining[0]["is_active"] = True

    await _save_connections(ctx, remaining)
    return ActionResult.success(
        DeleteResult(id=target, deleted=True, message=f"Disconnected Paycom connection {target}."), summary="Paycom disconnected."
    )
