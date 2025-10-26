#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
StackIt Constants and Configuration Classes.

This module provides enum-based constants and dataclass configurations
to replace string-based flags throughout the StackIt framework.
This improves type safety, IDE support, and maintainability while
preserving backward compatibility.
"""

from .constants import (
    # Enums
    Alignment,
    Orientation,
    SymbolRenderingMode,
    SymbolScale,
    SymbolWeight,
    MapType,
    BadgeType,
    # Configuration classes
    SFSymbolConfig,
    MapConfig,
    ChartConfig,
    LineChartConfig,
    BarChartConfig,
    RingChartConfig,
    # Conversion functions
    convert_alignment,
    convert_orientation,
    convert_rendering_mode,
    convert_symbol_scale,
    convert_symbol_weight,
    convert_map_type,
    convert_badge_type,
)

__all__ = [
    # Enums
    "Alignment",
    "Orientation",
    "SymbolRenderingMode",
    "SymbolScale",
    "SymbolWeight",
    "MapType",
    "BadgeType",
    # Configuration classes
    "SFSymbolConfig",
    "MapConfig",
    "ChartConfig",
    "LineChartConfig",
    "BarChartConfig",
    "RingChartConfig",
    # Conversion functions
    "convert_alignment",
    "convert_orientation",
    "convert_rendering_mode",
    "convert_symbol_scale",
    "convert_symbol_weight",
    "convert_map_type",
    "convert_badge_type",
]