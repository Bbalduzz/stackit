#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Window StackIt Controls.

This module provides window controls for creating standalone NSWindow instances
and managing their layouts and content.
"""

from ._base import *


def window(
    title: str | None = None,
    size: tuple[int, int] = (600, 600),
    mask: int = AppKit.NSWindowStyleMaskTitled
    | AppKit.NSWindowStyleMaskClosable
    | AppKit.NSWindowStyleMaskMiniaturizable
    | AppKit.NSWindowStyleMaskResizable,
) -> AppKit.NSWindow:
    """Create a window with a title and size"""
    new_window = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(0, 0, *size),
        mask,
        AppKit.NSBackingStoreBuffered,
        False,
    )

    new_window.center()
    new_window.setTitlebarAppearsTransparent_(True)
    new_window.setTitleVisibility_(AppKit.NSWindowTitleHidden)
    new_window.setMovableByWindowBackground_(True)
    new_window.standardWindowButton_(AppKit.NSWindowCloseButton).setHidden_(False)
    new_window.standardWindowButton_(AppKit.NSWindowMiniaturizeButton).setHidden_(False)
    new_window.standardWindowButton_(AppKit.NSWindowZoomButton).setHidden_(False)

    new_window.makeKeyAndOrderFront_(None)
    if title is not None:
        new_window.setTitle_(title)

    return new_window


def window_layout(
    window: AppKit.NSWindow,
    layout: AppKit.NSView,
    padding: tuple[float, float, float, float] = (20.0, 20.0, 20.0, 20.0),
) -> AppKit.NSView:
    """Add a layout (stack or single control) to a window with proper constraints.

    This helper function simplifies adding StacKit layouts to windows by handling
    all the constraint setup automatically.

    Args:
        window: The NSWindow to add the layout to
        layout: A StackView (from hstack/vstack) or any NSView control
        padding: Edge insets as (top, leading, bottom, trailing) in points

    Returns:
        The layout view that was added (for reference)

    Example:
        >>> win = stackit.window(title="My App", size=(400, 300))
        >>> content = stackit.vstack([
        ...     stackit.label("Username:", bold=True),
        ...     stackit.text_field(placeholder="Enter username"),
        ...     stackit.button("Submit", callback=submit_handler)
        ... ], spacing=12.0)
        >>> stackit.window_layout(win, content, padding=(20, 20, 20, 20))
        >>> win.makeKeyAndOrderFront_(None)
    """
    # Ensure layout doesn't translate autoresizing mask
    layout.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Add layout to window's content view
    content_view = window.contentView()
    content_view.addSubview_(layout)

    # Unpack padding
    top, leading, bottom, trailing = padding

    # Pin layout to content view with padding
    layout.topAnchor().constraintEqualToAnchor_constant_(
        content_view.topAnchor(), top
    ).setActive_(True)
    layout.bottomAnchor().constraintEqualToAnchor_constant_(
        content_view.bottomAnchor(), -bottom
    ).setActive_(True)
    layout.leadingAnchor().constraintEqualToAnchor_constant_(
        content_view.leadingAnchor(), leading
    ).setActive_(True)
    layout.trailingAnchor().constraintEqualToAnchor_constant_(
        content_view.trailingAnchor(), -trailing
    ).setActive_(True)

    return layout