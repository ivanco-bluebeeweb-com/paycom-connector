"""Entrypoint for Paycom Connector validation and deployment."""
import os, sys

_EXT_DIR = os.path.dirname(os.path.abspath(__file__))
if _EXT_DIR not in sys.path:
    sys.path.insert(0, _EXT_DIR)

for _mod in (
    "app", "schemas", "paycom_client", "handlers_connection",
    "handlers_resources", "panels", "panels_settings",
):
    sys.modules.pop(_mod, None)

from app import ext, chat  # noqa: E402,F401
import handlers_connection  # noqa: E402,F401
import handlers_resources   # noqa: E402,F401
import panels               # noqa: E402,F401
import panels_settings      # noqa: E402,F401
