from __future__ import annotations

import json
import os
import platform
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

DEFAULT_SERVER = "http://127.0.0.1:12315"


def _parse_server(server: str) -> tuple[str, int]:
    """Parse a server URL string into (host, port).

    Supported formats:
      - "http://10.191.64.81:12315"  → host="10.191.64.81", port=12315
      - "https://example.com"        → host="example.com", port=443
      - "http://example.com"         → host="example.com", port=80
      - "http://example.com:8080"    → host="example.com", port=8080
      - "127.0.0.1:12315"            → host="127.0.0.1", port=12315 (legacy shorthand)
      - "127.0.0.1"                  → host="127.0.0.1", port=12315 (bare host → default)
      - "" / empty                    → returns DEFAULT_SERVER parsed

    Port defaults:
      - http → 80
      - https → 443
      - no scheme (legacy shorthand) → 12315
    """
    if not server or not server.strip():
        return _parse_server(DEFAULT_SERVER)

    server = server.strip()

    # If no scheme, treat as legacy shorthand "host:port" or "host"
    if not server.startswith(("http://", "https://")):
        if ":" in server:
            last_colon = server.rfind(":")
            host = server[:last_colon].strip()
            port_str = server[last_colon + 1:].strip()
            if not host:
                raise ValueError(f"Invalid server '{server}': host cannot be empty")
            if re.search(r"[\s\x00-\x1f]", host):
                raise ValueError(f"Invalid host '{host}': must not contain spaces or control characters")
            if port_str:
                try:
                    port = int(port_str)
                except ValueError:
                    raise ValueError(f"Invalid server '{server}': port '{port_str}' is not a valid integer")
                if port < 1 or port > 65535:
                    raise ValueError(f"Invalid server '{server}': port must be between 1 and 65535, got {port}")
            else:
                port = 12315
        else:
            # Bare hostname with no scheme → use default
            host = server
            port = 12315

        if re.search(r"[\s\x00-\x1f]", host):
            raise ValueError(f"Invalid host '{host}': must not contain spaces or control characters")
        return host, port

    # Has scheme: parse as URL
    parsed = urlparse(server)
    scheme = parsed.scheme
    host = parsed.hostname

    if not host:
        raise ValueError(f"Invalid server '{server}': could not determine host")
    if re.search(r"[\s\x00-\x1f]", host):
        raise ValueError(f"Invalid host '{host}': must not contain spaces or control characters")

    if parsed.port:
        port = parsed.port
        if port < 1 or port > 65535:
            raise ValueError(f"Invalid server '{server}': port must be between 1 and 65535, got {port}")
    else:
        # Default port by scheme
        port = 443 if scheme == "https" else 80

    return host, port


def _validate_server(server: str) -> None:
    """Validate server string at the config layer. Raises ValueError on invalid input."""
    if not server or not server.strip():
        raise ValueError("Server address cannot be empty.")
    _parse_server(server)  # Will raise ValueError if invalid


def get_config_dir() -> Path:
    override = os.environ.get("LOGSEQ_CLI_CONFIG_DIR")
    if override:
        return Path(override)

    system = platform.system()
    home = Path.home()

    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "logseq-cli"
        return home / "AppData" / "Roaming" / "logseq-cli"

    if system == "Darwin":
        return home / "Library" / "Application Support" / "logseq-cli"

    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / "logseq-cli"
    return home / ".config" / "logseq-cli"


def get_config_path() -> Path:
    return get_config_dir() / "config.json"


def load_config() -> dict[str, Any]:
    path = get_config_path()
    if not path.exists():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    return data if isinstance(data, dict) else {}


def save_config(config: dict[str, Any]) -> Path:
    path = get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def set_token(token: str) -> Path:
    config = load_config()
    config["token"] = token
    return save_config(config)


def get_token() -> str | None:
    token = load_config().get("token")
    return token if isinstance(token, str) and token else None


def set_server(server: str) -> Path:
    _validate_server(server)
    config = load_config()
    config["server"] = server
    # Clean up legacy host/port keys
    config.pop("host", None)
    config.pop("port", None)
    return save_config(config)


def get_server() -> str:
    config = load_config()

    # Prefer new 'server' key
    server = config.get("server")
    if isinstance(server, str) and server:
        return server

    # Backward compatibility: reconstruct from legacy host + port
    host = config.get("host")
    port = config.get("port")
    if isinstance(host, str) and host and isinstance(port, int) and 1 <= port <= 65535:
        return f"http://{host}:{port}"

    return DEFAULT_SERVER


def resolve_server() -> tuple[str, int]:
    """Resolve the current server into (host, port) tuple, applying env var override."""
    env_server = os.environ.get("LOGSEQ_SERVER")
    server_str = env_server if env_server else get_server()

    # Validate env var server
    if env_server:
        try:
            return _parse_server(env_server)
        except ValueError as e:
            raise ValueError(f"Invalid LOGSEQ_SERVER '{env_server}': {e}")

    return _parse_server(server_str)
