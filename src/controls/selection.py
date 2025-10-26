#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Selection StackIt Controls.

This module provides selection controls like radio buttons and radio groups
for single and multiple choice user selections.
"""

from ._base import *


def radio_button(
    title: str = "",
    selected: bool = False,
    group=None,
    callback=None,
    **kwargs
) -> NSButton:
    """Create a radio button.

    Args:
        title: Radio button label
        selected: Whether initially selected
        group: Radio button group (for mutual exclusion)
        callback: Function called when selected
        **kwargs: Additional NSButton attributes (setXXX methods)

    Returns:
        NSButton configured as radio button
    """
    radio = NSButton.alloc().init()
    radio.setTitle_(title)
    radio.setButtonType_(AppKit.NSButtonTypeRadio)
    radio.setState_(AppKit.NSControlStateValueOn if selected else AppKit.NSControlStateValueOff)
    radio.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Apply additional attributes
    for method, value in kwargs.items():
        if hasattr(radio, method):
            getattr(radio, method)(value)

    if callback:
        radio.setTarget_(NSApp)
        radio.setAction_("radioButtonCallback:")
        StackAppDelegate.register_callback(radio, None, callback)

    return radio


def radio_group(
    options: list[str] | list,
    selected: int = 0,
    orientation: Union[str, Orientation] = Orientation.VERTICAL,
    spacing: float = 8.0,
    callback=None,
    **kwargs,
) -> "StackView":
    """Create a group of mutually exclusive radio buttons

    Args:
        options: List of radio button labels (strings) or pre-configured NSButton radio buttons
        selected: Index of initially selected option (default: 0)
        orientation: Layout orientation (Orientation enum or legacy string)
                    Use Orientation.VERTICAL or Orientation.HORIZONTAL
        spacing: Spacing between radio buttons in points (default: 8.0)
        callback: Python function called when selection changes.
                  Receives the NSButton that was selected.
        **kwargs: Additional keyword/value attributes (only applied when options are strings)

    Returns: StackView containing the radio button group
    """
    from core import hstack, vstack

    # Create radio buttons
    radio_buttons = []
    for i, option in enumerate(options):
        if isinstance(option, str):
            # Create radio button from string
            radio = radio_button(title=option, selected=(i == selected), **kwargs)
        elif isinstance(option, NSButton):
            # Use pre-configured radio button
            radio = option
            if i == selected:
                radio.setState_(AppKit.NSControlStateValueOn)
        else:
            continue
        radio_buttons.append(radio)

    # Create callback function that handles mutual exclusion
    def create_radio_callback(index, buttons):
        def radio_selected(sender):
            # Ensure mutual exclusion
            for j, button in enumerate(buttons):
                if j == index:
                    button.setState_(AppKit.NSControlStateValueOn)
                else:
                    button.setState_(AppKit.NSControlStateValueOff)

            # Call user callback if provided
            if callback:
                try:
                    callback(sender)
                except Exception as e:
                    Foundation.NSLog(f"Error in radio group callback: {e}")

        return radio_selected

    # Register callbacks for each button
    for i, rb in enumerate(radio_buttons):
        rb.setTarget_(NSApp)
        rb.setAction_("radioGroupCallback:")
        StackAppDelegate.register_callback(
            rb, None, create_radio_callback(i, radio_buttons)
        )

    # Create stack layout
    # Convert to enum if string, with deprecation warning
    orientation_enum = convert_orientation(orientation)
    if orientation_enum == Orientation.HORIZONTAL:
        container = hstack(radio_buttons, spacing=spacing)
    else:
        container = vstack(radio_buttons, spacing=spacing)

    return container