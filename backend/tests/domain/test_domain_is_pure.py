"""The documented boundary: domain/ depends only on the stdlib (minus I/O and the wall
clock) and python-chess. See DESIGN.md."""

import ast
import sys
from pathlib import Path

DOMAIN_DIR = Path(__file__).resolve().parents[2] / "pawnup" / "domain"
ALLOWED_THIRD_PARTY = {"chess", "pawnup"}
FORBIDDEN_STDLIB = {
    "asyncio", "time", "datetime", "socket", "threading", "sqlite3", "http", "urllib",
    "subprocess", "random", "os", "sched", "select", "ssl", "multiprocessing",
}  # fmt: skip


def violations(source: str) -> list[str]:
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            modules = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            modules = [node.module or ""]
        else:
            continue
        for module in modules:
            top = module.split(".")[0]
            if top == "pawnup":
                if not module.startswith("pawnup.domain") and module != "pawnup.ports":
                    found.append(module)
            else:
                unknown = top not in sys.stdlib_module_names and top not in ALLOWED_THIRD_PARTY
                if top in FORBIDDEN_STDLIB or unknown:
                    found.append(module)
    return found


def test_domain_modules_import_nothing_forbidden():
    files = sorted(DOMAIN_DIR.glob("*.py"))
    assert files, "domain/ not found"
    bad = {f.name: violations(f.read_text()) for f in files if violations(f.read_text())}
    assert bad == {}


def test_checker_catches_forbidden_imports():
    assert violations("import fastapi") == ["fastapi"]
    assert violations("from sqlalchemy import select") == ["sqlalchemy"]
    assert violations("import time") == ["time"]
    assert violations("from datetime import datetime") == ["datetime"]
    assert violations("import asyncio") == ["asyncio"]
    assert violations("from pawnup.adapters.db import x") == ["pawnup.adapters.db"]
    assert violations("import chess\nfrom dataclasses import dataclass") == []
