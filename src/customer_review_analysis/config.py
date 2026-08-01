from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config.yaml"


def _load_config() -> Dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


CONFIG = _load_config()


def get_repo_root() -> Path:
    return REPO_ROOT


def get_path(key: str, default: str | None = None) -> Path:
    env_key = f"CUSTOMER_REVIEW_{key.upper()}"
    env_value = os.getenv(env_key)
    if env_value:
        return Path(env_value).expanduser().resolve()

    value = CONFIG.get("paths", {}).get(key, default)
    if value is None:
        return REPO_ROOT
    return (REPO_ROOT / value).resolve()


def get_config() -> Dict[str, Any]:
    return CONFIG


def get_model_path(default: str | None = None) -> Path:
    env_value = os.getenv("CUSTOMER_REVIEW_MODEL_PATH")
    if env_value:
        return Path(env_value).expanduser().resolve()
    configured = CONFIG.get("models", {}).get("app_model_path", default)
    if configured:
        return (REPO_ROOT / configured).resolve()
    return REPO_ROOT
