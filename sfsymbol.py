#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SFSymbol support for StackBar framework.

SF Symbols are Apple's system-provided icons that automatically adapt to the current appearance
and accessibility settings. They are available on macOS 11.0 and later.
"""

import Foundation
import AppKit
from Foundation import NSLog
from AppKit import NSImage, NSImageSymbolConfiguration, NSColor


class SFSymbol:
    """Helper class for creating SF Symbol images with extensive customization options.

    SF Symbols are Apple's system-provided icons that automatically adapt to the current appearance
    and accessibility settings. They are available on macOS 11.0 and later.
    """

    # Constants for weight values (NSFont.Weight equivalents)
    WEIGHT_MAP = {
        "ultraLight": -0.8,  # NSFontWeightUltraLight
        "thin": -0.6,  # NSFontWeightThin
        "light": -0.4,  # NSFontWeightLight
        "regular": 0.0,  # NSFontWeightRegular
        "medium": 0.23,  # NSFontWeightMedium
        "semibold": 0.3,  # NSFontWeightSemibold
        "bold": 0.4,  # NSFontWeightBold
        "heavy": 0.56,  # NSFontWeightHeavy
        "black": 0.62,  # NSFontWeightBlack
    }

    # NSImage.SymbolScale values
    SCALE_MAP = {
        "small": 1,  # NSImageSymbolScaleSmall
        "medium": 2,  # NSImageSymbolScaleMedium
        "large": 3,  # NSImageSymbolScaleLarge
    }

    # NSImage.SymbolColorRenderingMode values
    RENDERING_MODE_MAP = {
        "automatic": 0,  # Automatic
        "monochrome": 1,  # Monochrome
        "hierarchical": 2,  # Hierarchical
        "palette": 3,  # Palette
        "multicolor": 4,  # Multicolor
    }

    def __init__(
        self,
        name,
        rendering="automatic",
        color="#ffffff",
        palette_colors=None,
        accessibility_description=None,
        point_size=None,
        weight=None,
        scale=None,
        text_style=None,
    ):
        """Create an SF Symbol with customization options.

        :param name: The name of the SF Symbol (e.g., "turtle", "heart.fill", "gear")
        :param rendering: Symbol rendering mode - "automatic", "monochrome", "hierarchical", "palette", or "multicolor"
        :param color: Color for the symbol as hex string (e.g., "#ffffff") or RGB tuple (r, g, b) or (r, g, b, a)
                     For hierarchical mode: single color used as base with derived opacities
                     For monochrome mode: single color for the entire symbol
        :param palette_colors: List of colors for palette mode - each color applies to a different layer
                              Format: ["#FF0000", "#00FF00", "#0000FF"] or [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        :param accessibility_description: Optional accessibility description for the symbol
        :param point_size: Point size for the symbol (CGFloat)
        :param weight: Font weight - "ultraLight", "thin", "light", "regular", "medium", "semibold", "bold", "heavy", "black"
        :param scale: Symbol scale - "small", "medium", "large"
        :param text_style: Text style - "body", "caption1", "caption2", "footnote", "headline", "subheadline", "title1", "title2", "title3"
        """
        self.name = name
        self.rendering = rendering
        self.color = color
        self.palette_colors = palette_colors
        self.point_size = point_size
        self.weight = weight
        self.scale = scale
        self.text_style = text_style
        self.accessibility_description = accessibility_description or name.replace(
            ".", " "
        ).replace("_", " ")

        self._nsimage = self._create_nsimage()

    def _create_nsimage(self):
        """Create the NSImage from the SF Symbol with applied customizations."""
        try:
            # Check if SF Symbols are available (macOS 11.0+)
            if not hasattr(
                NSImage, "imageWithSystemSymbolName_accessibilityDescription_"
            ):
                NSLog(
                    "SFSymbol: System symbols not available on this macOS version (requires 11.0+)"
                )
                return None

            # Create base image using the class factory method
            image = NSImage.imageWithSystemSymbolName_accessibilityDescription_(
                self.name, self.accessibility_description
            )

            if image is None:
                NSLog(f'SFSymbol: System symbol "{self.name}" not found')
                return None

            # Apply symbol configuration if we have any customizations
            config = self._build_configuration()
            if config and hasattr(image, "imageWithSymbolConfiguration_"):
                configured_image = image.imageWithSymbolConfiguration_(config)
                if configured_image:
                    image = configured_image

            # Set reasonable default size for statusbar use
            image.setSize_((20, 20))
            return image

        except AttributeError:
            NSLog(
                "SFSymbol: System symbols not available on this macOS version (requires 11.0+)"
            )
            return None
        except Exception as e:
            NSLog(f'SFSymbol: Error creating symbol "{self.name}": {e}')
            return None

    def _build_configuration(self):
        """Build the complete symbol configuration by combining all requested traits."""
        # NSImageSymbolConfiguration is a separate class, not a subclass of NSImage
        if not hasattr(AppKit, "NSImageSymbolConfiguration"):
            return None

        try:
            config = None

            # 1. Start with size/weight/scale configuration
            base_config = self._create_size_weight_scale_config()
            if base_config:
                config = base_config

            # 2. Apply color configuration (hierarchical/palette automatically set rendering mode)
            color_config = self._create_color_config()
            if color_config:
                if config:
                    config = config.configurationByApplyingConfiguration_(color_config)
                else:
                    config = color_config

            # 3. Apply rendering mode configuration (only if no color config was applied)
            # Note: hierarchical and palette colors already set the rendering mode,
            # so we only apply rendering_config for multicolor or monochrome without explicit colors
            if not color_config:
                rendering_config = self._create_rendering_config()
                if rendering_config:
                    if config:
                        config = config.configurationByApplyingConfiguration_(
                            rendering_config
                        )
                    else:
                        config = rendering_config

            return config

        except Exception as e:
            NSLog(f'SFSymbol: Error creating configuration for "{self.name}": {e}')
            return None

    def _create_size_weight_scale_config(self):
        """Create configuration for size, weight, and scale using the correct factory methods."""
        try:
            # Point size + weight + scale (macOS 11+)
            if self.point_size is not None and self.weight is not None:
                ns_weight = self.WEIGHT_MAP.get(self.weight)
                if ns_weight is not None:
                    ns_scale = self.SCALE_MAP.get(self.scale, 0)  # 0 = unspecified
                    if hasattr(
                        NSImageSymbolConfiguration,
                        "configurationWithPointSize_weight_scale_",
                    ):
                        return NSImageSymbolConfiguration.configurationWithPointSize_weight_scale_(
                            float(self.point_size), ns_weight, ns_scale
                        )
                    elif hasattr(
                        NSImageSymbolConfiguration, "configurationWithPointSize_weight_"
                    ):
                        return NSImageSymbolConfiguration.configurationWithPointSize_weight_(
                            float(self.point_size), ns_weight
                        )

            # Text style + scale (macOS 11+)
            elif self.text_style is not None:
                # These would need to be the actual NSFont.TextStyle constants
                text_style_map = {
                    "body": "NSFontTextStyleBody",
                    "caption1": "NSFontTextStyleCaption1",
                    "caption2": "NSFontTextStyleCaption2",
                    "footnote": "NSFontTextStyleFootnote",
                    "headline": "NSFontTextStyleHeadline",
                    "subheadline": "NSFontTextStyleSubheadline",
                    "title1": "NSFontTextStyleTitle1",
                    "title2": "NSFontTextStyleTitle2",
                    "title3": "NSFontTextStyleTitle3",
                }
                ns_text_style = text_style_map.get(self.text_style)
                if ns_text_style:
                    if self.scale and hasattr(
                        NSImageSymbolConfiguration, "configurationWithTextStyle_scale_"
                    ):
                        ns_scale = self.SCALE_MAP.get(self.scale)
                        if ns_scale:
                            return NSImageSymbolConfiguration.configurationWithTextStyle_scale_(
                                ns_text_style, ns_scale
                            )
                    if hasattr(
                        NSImageSymbolConfiguration, "configurationWithTextStyle_"
                    ):
                        return NSImageSymbolConfiguration.configurationWithTextStyle_(
                            ns_text_style
                        )

            # Scale only (macOS 11+)
            elif self.scale is not None:
                ns_scale = self.SCALE_MAP.get(self.scale)
                if ns_scale and hasattr(
                    NSImageSymbolConfiguration, "configurationWithScale_"
                ):
                    return NSImageSymbolConfiguration.configurationWithScale_(ns_scale)

        except Exception as e:
            NSLog(f"SFSymbol: Error creating size/weight/scale config: {e}")

        return None

    def _create_rendering_config(self):
        """Create rendering mode configuration using the correct factory methods."""
        if self.rendering == "automatic":
            return None

        try:
            # Try convenience methods first (various macOS versions)
            if self.rendering == "multicolor" and hasattr(
                NSImageSymbolConfiguration, "preferringMulticolor"
            ):
                # macOS 12+
                return NSImageSymbolConfiguration.preferringMulticolor()
            elif self.rendering == "monochrome" and hasattr(
                NSImageSymbolConfiguration, "preferringMonochrome"
            ):
                # macOS 16+ (Ventura)
                return NSImageSymbolConfiguration.preferringMonochrome()
            # elif hasattr(NSImageSymbolConfiguration, 'configurationWithColorRenderingMode_'):
            else:
                mode = self.RENDERING_MODE_MAP.get(self.rendering)
                if mode is not None:
                    return (
                        NSImageSymbolConfiguration.configurationWithColorRenderingMode_(
                            mode
                        )
                    )

        except Exception as e:
            NSLog(f"SFSymbol: Error creating rendering config: {e}")

        return None

    def _create_color_config(self):
        """Create color configuration using the correct factory methods."""
        try:
            # Palette mode with multiple colors (macOS 12+)
            if self.palette_colors and hasattr(
                NSImageSymbolConfiguration, "configurationWithPaletteColors_"
            ):
                ns_colors = []
                for color in self.palette_colors:
                    ns_color = self._parse_color(color)
                    if ns_color:
                        ns_colors.append(ns_color)
                if ns_colors:
                    return NSImageSymbolConfiguration.configurationWithPaletteColors_(
                        ns_colors
                    )

            # Single color handling based on rendering mode
            elif self.color:
                ns_color = self._parse_color(self.color)
                if ns_color:
                    # Hierarchical: base color with derived opacities (macOS 12+)
                    if self.rendering == "hierarchical" and hasattr(
                        NSImageSymbolConfiguration,
                        "configurationWithHierarchicalColor_",
                    ):
                        return NSImageSymbolConfiguration.configurationWithHierarchicalColor_(
                            ns_color
                        )

                    # Monochrome/Palette: single color (macOS 12+)
                    elif hasattr(
                        NSImageSymbolConfiguration, "configurationWithPaletteColors_"
                    ):
                        return (
                            NSImageSymbolConfiguration.configurationWithPaletteColors_(
                                [ns_color]
                            )
                        )

        except Exception as e:
            NSLog(f"SFSymbol: Error creating color config: {e}")

        return None

    def _parse_color(self, color):
        """Parse color parameter into NSColor."""
        try:
            if isinstance(color, str) and color.startswith("#"):
                # Parse hex color
                hex_color = color[1:]
                if len(hex_color) == 6:
                    r = int(hex_color[0:2], 16) / 255.0
                    g = int(hex_color[2:4], 16) / 255.0
                    b = int(hex_color[4:6], 16) / 255.0
                    return NSColor.colorWithRed_green_blue_alpha_(r, g, b, 1.0)
                elif len(hex_color) == 8:
                    r = int(hex_color[0:2], 16) / 255.0
                    g = int(hex_color[2:4], 16) / 255.0
                    b = int(hex_color[4:6], 16) / 255.0
                    a = int(hex_color[6:8], 16) / 255.0
                    return NSColor.colorWithRed_green_blue_alpha_(r, g, b, a)
            elif isinstance(color, (tuple, list)) and len(color) >= 3:
                # Parse RGB/RGBA tuple
                r, g, b = color[:3]
                a = color[3] if len(color) > 3 else 1.0
                # Normalize values if they appear to be in 0-255 range
                if any(val > 1.0 for val in [r, g, b]):
                    r, g, b = r / 255.0, g / 255.0, b / 255.0
                if a > 1.0:
                    a = a / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, a)
        except Exception as e:
            NSLog(f'SFSymbol: Error parsing color "{color}": {e}')
        return None

    def __call__(self):
        """Return the NSImage for use in StackBar components."""
        return self._nsimage

    def __repr__(self):
        color_info = (
            f"palette_colors={self.palette_colors}"
            if self.palette_colors
            else f'color="{self.color}"'
        )
        return f'<SFSymbol: name="{self.name}", rendering="{self.rendering}", {color_info}>'

    @staticmethod
    def named(symbol_name, accessibility_description=None):
        """Create an NSImage from a system symbol name (legacy method).

        :param symbol_name: The name of the SF Symbol (e.g., "tortoise", "heart.fill", "gear")
        :param accessibility_description: Optional accessibility description for the symbol
        :return: NSImage object that can be used anywhere an image is expected in StackBar
        """
        symbol = SFSymbol(
            symbol_name, accessibility_description=accessibility_description
        )
        return symbol()
