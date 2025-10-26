#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Core StackIt components.

This module contains the fundamental building blocks of the StackIt framework:
- StackApp: Main application class
- MenuItem: Individual menu items
- StackView: Custom stack view with list-like methods
- Layout functions: hstack() and vstack()
"""

from .core import StackApp, MenuItem, StackView, hstack, vstack
from .delegate import StackAppDelegate

__all__ = [
    "StackApp",
    "MenuItem",
    "StackView",
    "hstack",
    "vstack",
    "StackAppDelegate",
]