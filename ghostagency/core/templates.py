"""
Shared templates module for Ghost Agency.

This module provides a single shared Jinja2Templates instance
that can be used across all modules to avoid template object
inconsistency issues.
"""

from __future__ import annotations
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Set up templates and static files
BASE_DIR = Path(__file__).resolve().parent.parent.parent
shared_templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Disable template caching to avoid unhashable type errors with complex objects
shared_templates.env.cache = None

__all__ = ["shared_templates"]
