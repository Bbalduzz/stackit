#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
StackIt Utilities.

This module provides utility functions for common tasks like:
- Alerts and notifications
- Timers and scheduling
- File operations
- Preferences management
- Color parsing
"""

from .utils import (
    alert,
    notification,
    quit_application,
    timer,
    after,
    every,
    choose_directory,
    save_preferences,
    load_preferences,
    parse_color,
)

__all__ = [
    "alert",
    "notification",
    "quit_application",
    "timer",
    "after",
    "every",
    "choose_directory",
    "save_preferences",
    "load_preferences",
    "parse_color",
]