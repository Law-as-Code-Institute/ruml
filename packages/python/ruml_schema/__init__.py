# SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH
# SPDX-License-Identifier: Apache-2.0
"""RUML JSON Schemas — draft 2020-12 schemas for .ruml, .ruml-result and .ruml-ext documents."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

__all__ = [
    "RUML_SCHEMA_PATH",
    "RUML_RESULT_SCHEMA_PATH",
    "RUML_EXT_SCHEMA_PATH",
    "load_ruml_schema",
    "load_ruml_result_schema",
    "load_ruml_ext_schema",
    "spec_version",
]

_HERE = Path(__file__).parent

RUML_SCHEMA_PATH = _HERE / "ruml.schema.json"
RUML_RESULT_SCHEMA_PATH = _HERE / "ruml-result.schema.json"
RUML_EXT_SCHEMA_PATH = _HERE / "ruml-ext.schema.json"


def load_ruml_schema() -> dict[str, Any]:
    """The schema for `.ruml` documents."""
    return json.loads(RUML_SCHEMA_PATH.read_text(encoding="utf-8"))


def load_ruml_result_schema() -> dict[str, Any]:
    """The schema for `.ruml-result` documents."""
    return json.loads(RUML_RESULT_SCHEMA_PATH.read_text(encoding="utf-8"))


def load_ruml_ext_schema() -> dict[str, Any]:
    """The schema for `.ruml-ext` documents."""
    return json.loads(RUML_EXT_SCHEMA_PATH.read_text(encoding="utf-8"))


def spec_version() -> str:
    """The RUML spec version the schemas describe, e.g. `"0.1"`."""
    return load_ruml_schema()["x-ruml-spec-version"]
