#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Layout StackIt Controls.

This module provides layout controls like block containers for organizing
and styling groups of UI elements.
"""

from ._base import *


def block(
    content_view,
    radius=8.0,
    padding=None,
    border_color=None,
    border_width=1.0,
    background_color=None,
):
    """Create a bordered and rounded container around content (like SwiftUI's menuBlock).

    Args:
        content_view: The view to wrap (can be a StackView or any NSView)
        radius: Corner radius in points (default: 8.0)
        padding: Padding as (top, leading, bottom, trailing) or single value for all sides
        border_color: Border color (default: subtle gray with transparency)
        background_color: Background color (default: subtle white with transparency)

    Returns:
        NSView containing the content with border and background
    """
    # Parse padding
    if padding is None:
        padding_top = padding_leading = padding_bottom = padding_trailing = 12.0
    elif isinstance(padding, (int, float)):
        padding_top = padding_leading = padding_bottom = padding_trailing = float(
            padding
        )
    elif len(padding) == 4:
        padding_top, padding_leading, padding_bottom, padding_trailing = padding
    else:
        raise ValueError(
            "padding must be a number or tuple of (top, leading, bottom, trailing)"
        )

    # Create container view
    container = NSView.alloc().init()
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)
    container.setWantsLayer_(True)

    # Set up layer styling
    layer = container.layer()
    layer.setCornerRadius_(radius)
    layer.setBorderWidth_(border_width)

    # Set border color (default: subtle gray)
    if border_color:
        border_ns_color = parse_color(border_color)
        # Apply default alpha if color was hex without alpha
        if (
            isinstance(border_color, str)
            and border_color.startswith("#")
            and len(border_color) == 7
        ):
            # Hex color without alpha, apply default alpha
            border_ns_color = border_ns_color.colorWithAlphaComponent_(0.5)
    else:
        # Default: subtle gray border with transparency
        border_ns_color = NSColor.colorWithWhite_alpha_(0.5, 0.3)

    layer.setBorderColor_(border_ns_color.CGColor())

    # Set background color (default: subtle white)
    if background_color:
        bg_ns_color = parse_color(background_color)
        # Apply default alpha if color was hex without alpha
        if (
            isinstance(background_color, str)
            and background_color.startswith("#")
            and len(background_color) == 7
        ):
            # Hex color without alpha, apply default alpha
            bg_ns_color = bg_ns_color.colorWithAlphaComponent_(0.3)
    else:
        # Default: subtle white background with transparency
        bg_ns_color = NSColor.colorWithWhite_alpha_(1.0, 0.05)

    layer.setBackgroundColor_(bg_ns_color.CGColor())

    # Add shadow for depth
    layer.setShadowColor_(NSColor.colorWithWhite_alpha_(0.0, 0.1).CGColor())
    layer.setShadowOffset_(NSMakeSize(0, -1))
    layer.setShadowRadius_(3.0)
    layer.setShadowOpacity_(1.0)

    # Add content view
    container.addSubview_(content_view)

    # Set up constraints with padding
    content_view.topAnchor().constraintEqualToAnchor_constant_(
        container.topAnchor(), padding_top
    ).setActive_(True)
    content_view.bottomAnchor().constraintEqualToAnchor_constant_(
        container.bottomAnchor(), -padding_bottom
    ).setActive_(True)
    content_view.leadingAnchor().constraintEqualToAnchor_constant_(
        container.leadingAnchor(), padding_leading
    ).setActive_(True)
    content_view.trailingAnchor().constraintEqualToAnchor_constant_(
        container.trailingAnchor(), -padding_trailing
    ).setActive_(True)

    return container