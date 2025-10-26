#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic StackIt Controls.

This module provides fundamental UI controls like labels, images, buttons,
spacers, and separators that form the building blocks of most interfaces.
"""

from ._base import *


def label(
    text: str = "",
    font_size: int = 13,
    bold: bool = False,
    color: str = None,
    width: int = None,
    height: int = None,
    alignment: str = "left",
) -> NSTextField:
    """Create a text label.

    Args:
        text: Label text
        font_size: Font size in points (default: 13)
        bold: Whether to use bold font (default: False)
        color: Text color as hex string or RGB tuple
        width: Fixed width in points (optional)
        height: Fixed height in points (optional)
        alignment: Text alignment - "left", "center", "right" (default: "left")

    Returns:
        NSTextField configured as a label
    """
    label = NSTextField.alloc().init()
    label.setStringValue_(str(text))
    label.setBezeled_(False)
    label.setDrawsBackground_(False)
    label.setEditable_(False)
    label.setSelectable_(False)
    label.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Set font
    if bold:
        font = NSFont.boldSystemFontOfSize_(font_size)
    else:
        font = NSFont.systemFontOfSize_(font_size)
    label.setFont_(font)

    # Set text color if provided
    if color:
        ns_color = parse_color(color)
        if ns_color:
            label.setTextColor_(ns_color)

    # Set alignment
    text_alignment_map = {
        "left": AppKit.NSTextAlignmentLeft,
        "center": AppKit.NSTextAlignmentCenter,
        "right": AppKit.NSTextAlignmentRight,
    }
    if alignment in text_alignment_map:
        label.setAlignment_(text_alignment_map[alignment])

    # Set size constraints if provided
    if width:
        label.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    if height:
        label.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    return label


def link(text: str, url: str) -> NSTextField:
    """Create a clickable link label.

    Args:
        text: Link text to display
        url: URL to open when clicked

    Returns:
        NSTextField configured as a clickable link
    """
    # Create attributed string with link
    attributed_string = Foundation.NSMutableAttributedString.alloc().initWithString_(text)
    attributed_string.addAttribute_value_range_(
        Foundation.NSLinkAttributeName, url, Foundation.NSMakeRange(0, len(text))
    )
    attributed_string.addAttribute_value_range_(
        Foundation.NSForegroundColorAttributeName,
        NSColor.linkColor(),
        Foundation.NSMakeRange(0, len(text))
    )

    # Create text field
    link_field = NSTextField.alloc().init()
    link_field.setAttributedStringValue_(attributed_string)
    link_field.setBezeled_(False)
    link_field.setDrawsBackground_(False)
    link_field.setEditable_(False)
    link_field.setSelectable_(True)
    link_field.setTranslatesAutoresizingMaskIntoConstraints_(False)

    return link_field


def image(image_path, width=None, height=None, scaling=None, border_radius=None):
    """Create an image view.

    Args:
        image_path: Path to image file, NSImage object, SFSymbol, or URL string
        width: Image width in points (optional)
        height: Image height in points (optional)
        scaling: Image scaling mode - "proportional", "fit", "fill", "none" (optional)
        border_radius: Corner radius for rounded image (optional)

    Returns:
        NSImageView containing the image
    """
    image_view = NSImageView.alloc().init()
    image_view.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Handle different image input types
    ns_image = None

    if isinstance(image_path, NSImage):
        # Already an NSImage
        ns_image = image_path
    elif hasattr(image_path, '__call__'):
        # SFSymbol object (callable)
        ns_image = image_path()
    elif isinstance(image_path, str):
        if image_path.startswith(('http://', 'https://')):
            # URL - download image
            try:
                response = httpx.get(image_path)
                if response.status_code == 200:
                    image_data = NSData.alloc().initWithBytes_length_(
                        response.content, len(response.content)
                    )
                    ns_image = NSImage.alloc().initWithData_(image_data)
            except Exception as e:
                print(f"Failed to load image from URL {image_path}: {e}")
        else:
            # File path
            if os.path.exists(image_path):
                ns_image = NSImage.alloc().initWithContentsOfFile_(image_path)
            else:
                # Try as SF Symbol name
                if hasattr(NSImage, 'imageWithSystemSymbolName_accessibilityDescription_'):
                    ns_image = NSImage.imageWithSystemSymbolName_accessibilityDescription_(
                        image_path, image_path
                    )

    if ns_image:
        image_view.setImage_(ns_image)

        # Set scaling mode
        if scaling:
            scaling_map = {
                "proportional": AppKit.NSImageScaleProportionallyDown,
                "fit": AppKit.NSImageScaleProportionallyUpOrDown,
                "fill": AppKit.NSImageScaleAxesIndependently,
                "none": AppKit.NSImageScaleNone,
            }
            if scaling in scaling_map:
                image_view.setImageScaling_(scaling_map[scaling])

        # Set size constraints
        if width:
            image_view.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
        if height:
            image_view.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

        # Apply border radius if specified
        if border_radius:
            image_view.setWantsLayer_(True)
            image_view.layer().setCornerRadius_(border_radius)
            image_view.layer().setMasksToBounds_(True)

    return image_view


def button(
    title: str = "",
    callback=None,
    image=None,
    width: int = None,
    height: int = None,
    style: str = "normal",
    target=None,
    action=None,
) -> NSButton:
    """Create a button.

    Args:
        title: Button text
        callback: Python function to call when clicked (recommended)
        image: Button image (NSImage, SFSymbol, or image path)
        width: Button width in points (optional)
        height: Button height in points (optional)
        style: Button style - "normal", "default", "borderless" (default: "normal")
        target: Target object for action (legacy, use callback instead)
        action: Action selector string (legacy, use callback instead)

    Returns:
        NSButton configured with the specified properties
    """
    # Use PersistentDefaultButton for default style to maintain appearance
    if style == "default":
        button = PersistentDefaultButton.alloc().init()
    else:
        button = NSButton.alloc().init()

    button.setTitle_(title)
    button.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Set button style
    if style == "default":
        button.setBezelStyle_(AppKit.NSBezelStyleRounded)
        button.setKeyEquivalent_("\r")  # Return key
        if hasattr(button, 'set_persistent_key_equivalent'):
            button.set_persistent_key_equivalent(True)
    elif style == "borderless":
        button.setBezelStyle_(AppKit.NSBezelStyleInline)
        button.setBordered_(False)
    else:  # normal
        button.setBezelStyle_(AppKit.NSBezelStyleRounded)

    # Set image if provided
    if image:
        if isinstance(image, NSImage):
            button.setImage_(image)
        elif hasattr(image, '__call__'):  # SFSymbol
            button.setImage_(image())
        elif isinstance(image, str):
            # Try to load as SF Symbol or file
            if hasattr(NSImage, 'imageWithSystemSymbolName_accessibilityDescription_'):
                sf_image = NSImage.imageWithSystemSymbolName_accessibilityDescription_(
                    image, image
                )
                if sf_image:
                    button.setImage_(sf_image)
            elif os.path.exists(image):
                ns_image = NSImage.alloc().initWithContentsOfFile_(image)
                if ns_image:
                    button.setImage_(ns_image)

    # Set size constraints
    if width:
        button.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    if height:
        button.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    # Set up callback or target/action
    if callback:
        # Modern callback approach (recommended)
        button.setTarget_(NSApp)
        button.setAction_("buttonCallback:")
        StackAppDelegate.register_callback(button, None, callback)
    elif target and action:
        # Legacy target/action approach
        button.setTarget_(target)
        button.setAction_(action)

    return button


def spacer(priority=250):
    """Create a flexible spacer view.

    Args:
        priority: Content hugging priority (lower = more expansion)

    Returns:
        NSView configured as a spacer
    """
    spacer_view = NSView.alloc().init()
    spacer_view.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Set content hugging priority to allow expansion
    spacer_view.setContentHuggingPriority_forOrientation_(
        priority, AppKit.NSLayoutConstraintOrientationHorizontal
    )
    spacer_view.setContentHuggingPriority_forOrientation_(
        priority, AppKit.NSLayoutConstraintOrientationVertical
    )

    return spacer_view


def separator(vertical=False):
    """Create a separator line.

    Args:
        vertical: Whether to create a vertical separator (default: False for horizontal)

    Returns:
        NSView configured as a separator line
    """
    separator_view = NSView.alloc().init()
    separator_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
    separator_view.setWantsLayer_(True)
    separator_view.layer().setBackgroundColor_(NSColor.separatorColor().CGColor())

    if vertical:
        # Vertical separator
        separator_view.widthAnchor().constraintEqualToConstant_(1).setActive_(True)
    else:
        # Horizontal separator
        separator_view.heightAnchor().constraintEqualToConstant_(1).setActive_(True)

    return separator_view