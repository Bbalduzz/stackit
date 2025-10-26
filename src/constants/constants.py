#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
StackIt Constants and Configuration Classes

This module provides enum-based constants and dataclass configurations
to replace string-based flags throughout the StackIt framework.
This improves type safety, IDE support, and maintainability while
preserving backward compatibility.
"""

from enum import Enum, StrEnum
from dataclasses import dataclass
from typing import Optional, Union, List, Tuple
import warnings

# Import AppKit constants for mapping
try:
    import AppKit
    APPKIT_AVAILABLE = True
except ImportError:
    APPKIT_AVAILABLE = False

try:
    import MapKit
    MAPKIT_AVAILABLE = True
except ImportError:
    MAPKIT_AVAILABLE = False


class Alignment(StrEnum):
    """Layout alignment options for stack views."""
    CENTER_X = "center_x"
    CENTER_Y = "center_y"
    LEADING = "leading"
    TRAILING = "trailing"

    @classmethod
    def from_string(cls, value: Union[str, 'Alignment']) -> 'Alignment':
        """Convert string to Alignment enum with backward compatibility."""
        if isinstance(value, cls):
            return value

        # Handle legacy string values
        legacy_map = {
            "center_x": cls.CENTER_X,
            "center_y": cls.CENTER_Y,
            "leading": cls.LEADING,
            "trailing": cls.TRAILING,
        }

        if value in legacy_map:
            return legacy_map[value]

        raise ValueError(f"Invalid alignment: {value}. Valid options: {list(legacy_map.keys())}")

    def to_appkit_constant(self):
        """Convert to AppKit layout attribute constant."""
        if not APPKIT_AVAILABLE:
            return None

        mapping = {
            self.CENTER_X: AppKit.NSLayoutAttributeCenterX,
            self.CENTER_Y: AppKit.NSLayoutAttributeCenterY,
            self.LEADING: AppKit.NSLayoutAttributeLeading,
            self.TRAILING: AppKit.NSLayoutAttributeTrailing,
        }
        return mapping.get(self)


class Orientation(StrEnum):
    """Layout orientation options."""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

    @classmethod
    def from_string(cls, value: Union[str, 'Orientation']) -> 'Orientation':
        """Convert string to Orientation enum with backward compatibility."""
        if isinstance(value, cls):
            return value

        if value in ["horizontal", "vertical"]:
            return cls(value)

        raise ValueError(f"Invalid orientation: {value}. Valid options: horizontal, vertical")


class SymbolRenderingMode(StrEnum):
    """SF Symbol rendering mode options."""
    AUTOMATIC = "automatic"
    MONOCHROME = "monochrome"
    HIERARCHICAL = "hierarchical"
    PALETTE = "palette"
    MULTICOLOR = "multicolor"

    @classmethod
    def from_string(cls, value: Union[str, 'SymbolRenderingMode']) -> 'SymbolRenderingMode':
        """Convert string to SymbolRenderingMode enum with backward compatibility."""
        if isinstance(value, cls):
            return value

        if value in ["automatic", "monochrome", "hierarchical", "palette", "multicolor"]:
            return cls(value)

        raise ValueError(f"Invalid rendering mode: {value}. Valid options: {[m.value for m in cls]}")

    def to_appkit_constant(self):
        """Convert to AppKit rendering mode constant."""
        mapping = {
            self.AUTOMATIC: 0,
            self.MONOCHROME: 1,
            self.HIERARCHICAL: 2,
            self.PALETTE: 3,
            self.MULTICOLOR: 4,
        }
        return mapping.get(self)


class SymbolScale(StrEnum):
    """SF Symbol scale options."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

    @classmethod
    def from_string(cls, value: Union[str, 'SymbolScale']) -> 'SymbolScale':
        """Convert string to SymbolScale enum with backward compatibility."""
        if isinstance(value, cls):
            return value

        if value in ["small", "medium", "large"]:
            return cls(value)

        raise ValueError(f"Invalid scale: {value}. Valid options: small, medium, large")

    def to_appkit_constant(self):
        """Convert to AppKit scale constant."""
        mapping = {
            self.SMALL: 1,
            self.MEDIUM: 2,
            self.LARGE: 3,
        }
        return mapping.get(self)


class SymbolWeight(StrEnum):
    """SF Symbol weight options."""
    ULTRA_LIGHT = "ultraLight"
    THIN = "thin"
    LIGHT = "light"
    REGULAR = "regular"
    MEDIUM = "medium"
    SEMIBOLD = "semibold"
    BOLD = "bold"
    HEAVY = "heavy"
    BLACK = "black"

    @classmethod
    def from_string(cls, value: Union[str, 'SymbolWeight']) -> 'SymbolWeight':
        """Convert string to SymbolWeight enum with backward compatibility."""
        if isinstance(value, cls):
            return value

        valid_values = [
            "ultraLight", "thin", "light", "regular", "medium",
            "semibold", "bold", "heavy", "black"
        ]

        if value in valid_values:
            return cls(value)

        raise ValueError(f"Invalid weight: {value}. Valid options: {valid_values}")

    def to_font_weight(self):
        """Convert to NSFont weight constant."""
        mapping = {
            self.ULTRA_LIGHT: -0.8,
            self.THIN: -0.6,
            self.LIGHT: -0.4,
            self.REGULAR: 0.0,
            self.MEDIUM: 0.23,
            self.SEMIBOLD: 0.3,
            self.BOLD: 0.4,
            self.HEAVY: 0.56,
            self.BLACK: 0.62,
        }
        return mapping.get(self)


class MapType(StrEnum):
    """Map view type options."""
    STANDARD = "standard"
    SATELLITE = "satellite"
    HYBRID = "hybrid"
    SATELLITE_FLYOVER = "satellite_flyover"
    HYBRID_FLYOVER = "hybrid_flyover"
    MUTED_STANDARD = "muted_standard"

    @classmethod
    def from_string(cls, value: Union[str, 'MapType']) -> 'MapType':
        """Convert string to MapType enum with backward compatibility."""
        if isinstance(value, cls):
            return value

        valid_values = [
            "standard", "satellite", "hybrid", "satellite_flyover",
            "hybrid_flyover", "muted_standard"
        ]

        if value in valid_values:
            return cls(value)

        raise ValueError(f"Invalid map type: {value}. Valid options: {valid_values}")

    def to_mapkit_constant(self):
        """Convert to MapKit constant."""
        if not MAPKIT_AVAILABLE:
            return None

        mapping = {
            self.STANDARD: MapKit.MKMapTypeStandard,
            self.SATELLITE: MapKit.MKMapTypeSatellite,
            self.HYBRID: MapKit.MKMapTypeHybrid,
        }

        # Handle newer map types with fallbacks
        if hasattr(MapKit, 'MKMapTypeSatelliteFlyover'):
            mapping[self.SATELLITE_FLYOVER] = MapKit.MKMapTypeSatelliteFlyover
        if hasattr(MapKit, 'MKMapTypeHybridFlyover'):
            mapping[self.HYBRID_FLYOVER] = MapKit.MKMapTypeHybridFlyover
        if hasattr(MapKit, 'MKMapTypeMutedStandard'):
            mapping[self.MUTED_STANDARD] = MapKit.MKMapTypeMutedStandard

        return mapping.get(self, MapKit.MKMapTypeStandard)


class BadgeType(StrEnum):
    """Menu item badge type options."""
    UPDATES = "updates"
    NEW_ITEMS = "new-items"
    ALERTS = "alerts"

    @classmethod
    def from_string(cls, value: Union[str, 'BadgeType']) -> 'BadgeType':
        """Convert string to BadgeType enum with backward compatibility."""
        if isinstance(value, cls):
            return value

        # Handle variations
        value_lower = value.lower().replace("-", "").replace("_", "")

        if value_lower in ["updates", "update"]:
            return cls.UPDATES
        elif value_lower in ["newitems", "new"]:
            return cls.NEW_ITEMS
        elif value_lower in ["alerts", "alert"]:
            return cls.ALERTS
        else:
            raise ValueError(f"Invalid badge type: {value}. Valid options: updates, new-items, alerts")

    def to_appkit_constant(self):
        """Convert to AppKit badge type constant."""
        if not APPKIT_AVAILABLE or not hasattr(AppKit, 'NSMenuItemBadgeTypeUpdates'):
            return None

        mapping = {
            self.UPDATES: AppKit.NSMenuItemBadgeTypeUpdates,
            self.NEW_ITEMS: AppKit.NSMenuItemBadgeTypeNewItems,
            self.ALERTS: AppKit.NSMenuItemBadgeTypeAlerts,
        }
        return mapping.get(self)


# Configuration dataclasses for complex components

@dataclass
class SFSymbolConfig:
    """Configuration for SF Symbol creation."""
    name: str
    rendering: Union[str, SymbolRenderingMode] = SymbolRenderingMode.AUTOMATIC
    color: Optional[str] = None
    palette_colors: Optional[List[str]] = None
    accessibility_description: Optional[str] = None
    point_size: Optional[float] = None
    weight: Optional[Union[str, SymbolWeight]] = None
    scale: Optional[Union[str, SymbolScale]] = None
    text_style: Optional[str] = None

    def __post_init__(self):
        """Convert string values to enums after initialization."""
        if isinstance(self.rendering, str):
            self.rendering = SymbolRenderingMode.from_string(self.rendering)
        if isinstance(self.weight, str) and self.weight is not None:
            self.weight = SymbolWeight.from_string(self.weight)
        if isinstance(self.scale, str) and self.scale is not None:
            self.scale = SymbolScale.from_string(self.scale)


@dataclass
class MapConfig:
    """Configuration for map view creation."""
    latitude: float
    longitude: float
    zoom: float = 0.05
    dimensions: Tuple[float, float] = (400, 300)
    map_type: Union[str, MapType] = MapType.STANDARD
    show_controls: bool = True
    border_radius: float = 0.0
    annotations: Optional[List[dict]] = None

    def __post_init__(self):
        """Convert string values to enums after initialization."""
        if isinstance(self.map_type, str):
            self.map_type = MapType.from_string(self.map_type)


@dataclass
class ChartConfig:
    """Base configuration for chart creation."""
    dimensions: Tuple[float, float] = (400, 300)
    max_value: Optional[float] = None
    min_value: Optional[float] = None
    color: str = "#007AFF"
    show_axes: bool = False
    show_grid: bool = False
    x_labels: Optional[List[str]] = None
    y_labels: Optional[List[Union[str, int, float]]] = None
    axis_color: Optional[str] = None
    grid_color: Optional[str] = None

    def __post_init__(self):
        """Base post-initialization - can be overridden by subclasses."""
        pass


@dataclass
class LineChartConfig(ChartConfig):
    """Configuration for line chart creation."""
    line_width: float = 2.0
    fill: bool = False
    points: Optional[List[Union[int, float]]] = None

    def __post_init__(self):
        """Validate that points are provided."""
        super().__post_init__()
        if self.points is None:
            raise ValueError("points must be provided for LineChartConfig")


@dataclass
class BarChartConfig(ChartConfig):
    """Configuration for bar chart creation."""
    bar_spacing: float = 2.0
    corner_radius: float = 0.0
    values: Optional[List[Union[int, float]]] = None

    def __post_init__(self):
        """Validate that values are provided."""
        super().__post_init__()
        if self.values is None:
            raise ValueError("values must be provided for BarChartConfig")


@dataclass
class RingChartConfig:
    """Configuration for ring chart creation."""
    data: List[Union[int, float]]
    dimensions: Tuple[float, float] = (120, 120)
    colors: Optional[List[str]] = None
    ring_width: float = 10.0
    spacing: float = 2.0
    labels: Optional[List[str]] = None


# Backward compatibility functions

def deprecation_warning(old_param: str, new_param: str):
    """Issue a deprecation warning for string-based parameters."""
    warnings.warn(
        f"Using string '{old_param}' is deprecated. Use {new_param} enum instead.",
        DeprecationWarning,
        stacklevel=3
    )


def convert_alignment(value: Union[str, Alignment], warn: bool = True) -> Alignment:
    """Convert alignment value with optional deprecation warning."""
    if isinstance(value, str) and warn:
        deprecation_warning(f"alignment='{value}'", "Alignment enum")
    return Alignment.from_string(value)


def convert_orientation(value: Union[str, Orientation], warn: bool = True) -> Orientation:
    """Convert orientation value with optional deprecation warning."""
    if isinstance(value, str) and warn:
        deprecation_warning(f"orientation='{value}'", "Orientation enum")
    return Orientation.from_string(value)


def convert_rendering_mode(value: Union[str, SymbolRenderingMode], warn: bool = True) -> SymbolRenderingMode:
    """Convert rendering mode value with optional deprecation warning."""
    if isinstance(value, str) and warn:
        deprecation_warning(f"rendering='{value}'", "SymbolRenderingMode enum")
    return SymbolRenderingMode.from_string(value)


def convert_symbol_scale(value: Union[str, SymbolScale], warn: bool = True) -> SymbolScale:
    """Convert symbol scale value with optional deprecation warning."""
    if isinstance(value, str) and warn:
        deprecation_warning(f"scale='{value}'", "SymbolScale enum")
    return SymbolScale.from_string(value)


def convert_symbol_weight(value: Union[str, SymbolWeight], warn: bool = True) -> SymbolWeight:
    """Convert symbol weight value with optional deprecation warning."""
    if isinstance(value, str) and warn:
        deprecation_warning(f"weight='{value}'", "SymbolWeight enum")
    return SymbolWeight.from_string(value)


def convert_map_type(value: Union[str, MapType], warn: bool = True) -> MapType:
    """Convert map type value with optional deprecation warning."""
    if isinstance(value, str) and warn:
        deprecation_warning(f"map_type='{value}'", "MapType enum")
    return MapType.from_string(value)


def convert_badge_type(value: Union[str, BadgeType], warn: bool = True) -> BadgeType:
    """Convert badge type value with optional deprecation warning."""
    if isinstance(value, str) and warn:
        deprecation_warning(f"badge='{value}'", "BadgeType enum")
    return BadgeType.from_string(value)


# Export all enums and configs for easy import
__all__ = [
    # Enums
    'Alignment',
    'Orientation',
    'SymbolRenderingMode',
    'SymbolScale',
    'SymbolWeight',
    'MapType',
    'BadgeType',

    # Configuration classes
    'SFSymbolConfig',
    'MapConfig',
    'ChartConfig',
    'LineChartConfig',
    'BarChartConfig',
    'RingChartConfig',

    # Conversion functions
    'convert_alignment',
    'convert_orientation',
    'convert_rendering_mode',
    'convert_symbol_scale',
    'convert_symbol_weight',
    'convert_map_type',
    'convert_badge_type',
]