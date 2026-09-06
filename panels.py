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
        trigger=ui.Button("How do I set this up?", variant="ghost", size="sm"),
        title="Connecting Paycom",
        children=[
            ui.Text(
                "1. Sign in to your Paycom account and navigate to API/Integration or OAuth settings.\n2. Choose your preferred authentication method (OAuth SSO, API Key / Personal Token, or Client Credentials / Service Account).\n3. Authorize or enter your credentials above and click Connect.",
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
            ui.Stack(
                direction="v",
                gap=1,
                align="stretch",
                children=[
                    ui.Text("Manage your Paycom connections and integrations.", variant="caption"),
                ]
            ),
            ui.Divider(),
            ui.Stack(
                direction="v",
                gap=2,
                align="stretch",
                children=[
                    ui.Button(
                        "Sign in with Paycom (OAuth / SSO)",
                        variant="primary",
                        size="sm",
                        icon="login"
                    ),
                    ui.Divider(),
                    ui.Text("Or connect via API Key or Service Account", variant="caption"),
                    ui.Form(
                        submit_label="Connect Paycom",
                        action=ui.Call("connect_paycom"),
                        children=[
                            ui.Stack(
                                direction="v",
                                gap=2,
                                align="stretch",
                                children=[
                                    ui.Stack(
                                        direction="v",
                                        gap=1,
                                        align="stretch",
                                        children=[
                                            ui.Text("Authentication Method", variant="label"),
                                            ui.Select(
                                                param_name="auth_mode",
                                                value="api_key",
                                                options=[
                                                    {"label": "API Key / Personal Access Token", "value": "api_key"},
                                                    {"label": "OAuth 2.0 Bearer Token", "value": "oauth"},
                                                    {"label": "Client Credentials (Service Account / Machine-to-Machine)", "value": "client_credentials"},
                                                ]
                                            ),
                                        ]
                                    ),
                                    ui.Stack(
                                        direction="v",
                                        gap=1,
                                        align="stretch",
                                        children=[
                                            ui.Text("Connection Label", variant="label"),
                                            ui.Input(param_name="label", placeholder="e.g. Production Paycom"),
                                        ]
                                    ),
                                    ui.Stack(
                                        direction="v",
                                        gap=1,
                                        align="stretch",
                                        children=[
                                            ui.Text("API Key / Access Token", variant="label"),
                                            ui.Input(param_name="api_key", placeholder="Paste API Key, Bearer or Access Token"),
                                        ]
                                    ),
                                ]
                            )
                        ]
                    ),
                ]
            ),
            _help_modal(),
            ui.Spacer(),
            _settings_button(),
        ]
    )
