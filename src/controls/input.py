#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Input StackIt Controls.

This module provides input controls like text fields, sliders, checkboxes,
and other interactive elements for user input.
"""

from ._base import *


def text_field(
    text: str = "",
    placeholder: str = "",
    width: int = 200,
    height: int = 22,
    multiline: bool = False,
    scroll: bool = True,
    editable: bool = True,
    callback=None,
) -> Union[NSTextField, ScrollViewWithTextView]:
    """Create a text input field.

    Args:
        text: Initial text content
        placeholder: Placeholder text when empty
        width: Field width in points
        height: Field height in points
        multiline: Whether to allow multiple lines
        scroll: Whether to show scroll bars (for multiline)
        editable: Whether the text can be edited
        callback: Function called when text changes

    Returns:
        NSTextField for single line, ScrollViewWithTextView for multiline
    """
    if multiline:
        # Create scrollable text view for multiline
        scroll_view = ScrollViewWithTextView.alloc().initWithSize_VScroll_(
            (width, height), scroll
        )
        scroll_view.setString_(text)
        scroll_view.setEditable_(editable)

        if callback:
            # Register callback for text changes
            StackAppDelegate.register_callback(scroll_view, None, callback)

        return scroll_view
    else:
        # Create single-line text field
        text_field = NSTextField.alloc().init()
        text_field.setStringValue_(text)
        if placeholder:
            text_field.setPlaceholderString_(placeholder)
        text_field.setEditable_(editable)
        text_field.setSelectable_(True)
        text_field.setBezeled_(True)
        text_field.setBezelStyle_(AppKit.NSTextFieldSquareBezel)
        text_field.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Set size constraints
        text_field.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
        text_field.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

        if callback:
            text_field.setTarget_(NSApp)
            text_field.setAction_("textFieldCallback:")
            StackAppDelegate.register_callback(text_field, None, callback)

        return text_field


def secure_text_input(text="", placeholder="", width=200, height=22, callback=None):
    """Create a secure text input field (password field).

    Args:
        text: Initial text content
        placeholder: Placeholder text when empty
        width: Field width in points
        height: Field height in points
        callback: Function called when text changes

    Returns:
        NSSecureTextField for password input
    """
    secure_field = NSSecureTextField.alloc().init()
    secure_field.setStringValue_(text)
    if placeholder:
        secure_field.setPlaceholderString_(placeholder)
    secure_field.setBezeled_(True)
    secure_field.setBezelStyle_(AppKit.NSTextFieldSquareBezel)
    secure_field.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Set size constraints
    secure_field.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    secure_field.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    if callback:
        secure_field.setTarget_(NSApp)
        secure_field.setAction_("textFieldCallback:")
        StackAppDelegate.register_callback(secure_field, None, callback)

    return secure_field


def search_field(
    text: str = "",
    placeholder: str = "Search...",
    width: int = 200,
    height: int = 22,
    callback=None,
) -> NSSearchField:
    """Create a search field with search icon.

    Args:
        text: Initial search text
        placeholder: Placeholder text when empty
        width: Field width in points
        height: Field height in points
        callback: Function called when search text changes

    Returns:
        NSSearchField configured for search input
    """
    search_field = NSSearchField.alloc().init()
    search_field.setStringValue_(text)
    if placeholder:
        search_field.setPlaceholderString_(placeholder)
    search_field.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Set size constraints
    search_field.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    search_field.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    if callback:
        search_field.setTarget_(NSApp)
        search_field.setAction_("textFieldCallback:")
        StackAppDelegate.register_callback(search_field, None, callback)

    return search_field


def slider(value=50, min_value=0, max_value=100, width=180, height=15, callback=None):
    """Create a horizontal slider.

    Args:
        value: Initial slider value
        min_value: Minimum slider value
        max_value: Maximum slider value
        width: Slider width in points
        height: Slider height in points
        callback: Function called when value changes

    Returns:
        NSSlider configured with the specified range and value
    """
    slider = NSSlider.alloc().init()
    slider.setMinValue_(min_value)
    slider.setMaxValue_(max_value)
    slider.setDoubleValue_(value)
    slider.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Set size constraints
    slider.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    slider.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    if callback:
        slider.setTarget_(NSApp)
        slider.setAction_("sliderCallback:")
        StackAppDelegate.register_callback(slider, None, callback)

    return slider


def checkbox(title="", checked=False, callback=None):
    """Create a checkbox.

    Args:
        title: Checkbox label text
        checked: Initial checked state
        callback: Function called when state changes

    Returns:
        NSButton configured as a checkbox
    """
    checkbox = NSButton.alloc().init()
    checkbox.setTitle_(title)
    checkbox.setButtonType_(AppKit.NSButtonTypeSwitch)
    checkbox.setState_(AppKit.NSControlStateValueOn if checked else AppKit.NSControlStateValueOff)
    checkbox.setTranslatesAutoresizingMaskIntoConstraints_(False)

    if callback:
        checkbox.setTarget_(NSApp)
        checkbox.setAction_("checkboxCallback:")
        StackAppDelegate.register_callback(checkbox, None, callback)

    return checkbox


def combobox(
    items: list = None,
    selected: str = "",
    editable: bool = True,
    width: int = 200,
    height: int = 26,
    callback=None,
) -> NSComboBox:
    """Create a combo box (dropdown with optional text input).

    Args:
        items: List of items to show in dropdown
        selected: Initially selected item
        editable: Whether user can type custom values
        width: Combo box width in points
        height: Combo box height in points
        callback: Function called when selection changes

    Returns:
        NSComboBox configured with the specified items
    """
    combo = NSComboBox.alloc().init()
    combo.setEditable_(editable)
    combo.setTranslatesAutoresizingMaskIntoConstraints_(False)

    if items:
        combo.addItemsWithObjectValues_(items)

    if selected and selected in (items or []):
        combo.selectItemWithObjectValue_(selected)
    elif selected:
        combo.setStringValue_(selected)

    # Set size constraints
    combo.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    combo.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    if callback:
        combo.setTarget_(NSApp)
        combo.setAction_("comboboxCallback:")
        StackAppDelegate.register_callback(combo, None, callback)

    return combo