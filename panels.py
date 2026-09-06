"""Panel UI for Paycom Connector following UI_INTERFACE_STANDARD.md and AUTH_AND_CREDENTIALS_STANDARD.md."""
from __future__ import annotations
from imperal_sdk import ui
from app import ext

def _settings_button() -> ui.UINode:
    return ui.Button(
        "App settings",
        variant="secondary",
        size="sm",
        icon="settings",
        on_click=ui.Call("__panel__paycom_settings")
    )

def _help_modal() -> ui.UINode:
    return ui.Modal(
        trigger=ui.Button("How do I connect Paycom?", variant="ghost", size="sm"),
        title="Connecting Paycom",
        children=[
            ui.Text(
                "1. Sign in to your Paycom Client Portal at paycomonline.net.\n"
                "2. Your Client Code (e.g. 4-6 alphanumeric code) is located in the client header.\n"
                "3. Under System Settings > API Integrations, generate an API Bearer Token.\n"
                "4. Enter your API Token and Client Code above and click Connect Paycom.",
                variant="body"
            )
        ]
    )

@ext.panel("paycom_sidebar", slot="left")
async def paycom_sidebar(ctx, **kwargs) -> ui.UINode:
    return ui.Stack(
        direction="v",
        gap=3,
        align="stretch",
        children=[
            ui.Text("Paycom", variant="heading"),
            ui.Text("Manage workforce, employees, payroll runs, departments, time-off and direct deposits via Paycom REST API.", variant="caption"),
            ui.Divider(),
            ui.Form(
                submit_label="Connect Paycom",
                action=ui.Call("connect_paycom"),
                children=[
                    ui.Stack(
                        direction="v",
                        gap=2,
                        align="stretch",
                        children=[
                            ui.Text("Connection Label", variant="caption"),
                            ui.Input(
                                param_name="label",
                                placeholder="e.g. Acme Paycom",
                                value=""
                            ),
                            ui.Text("API Bearer Token", variant="caption"),
                            ui.Input(
                                param_name="api_token",
                                placeholder="Enter Paycom API Token",
                                type="password",
                                value=""
                            ),
                            ui.Text("Client Code", variant="caption"),
                            ui.Input(
                                param_name="client_code",
                                placeholder="e.g. ACM01",
                                value=""
                            ),
                            ui.Text("Custom Base URL (optional)", variant="caption"),
                            ui.Input(
                                param_name="base_url",
                                placeholder="https://api.paycom.com",
                                value=""
                            ),
                        ]
                    )
                ]
            ),
            ui.Divider(),
            ui.Stack(
                direction="h",
                gap=2,
                children=[
                    _settings_button(),
                    _help_modal(),
                ]
            )
        ]
    )
