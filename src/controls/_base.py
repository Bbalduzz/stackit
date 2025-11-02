#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base classes and shared functionality for StackIt controls.

This module contains common base classes, utilities, and constants
used across multiple control implementations.
"""

import Foundation
import AppKit
from Foundation import NSMakeRect, NSMakeSize, NSMakePoint, NSData, NSNumber
from AppKit import (
    NSObject,
    NSView,
    NSTextField,
    NSFont,
    NSColor,
    NSImage,
    NSImageView,
    NSButton,
    NSSlider,
    NSProgressIndicator,
    NSComboBox,
    NSBezierPath,
    NSRoundLineCapStyle,
    NSTextView,
    NSScrollView,
    NSSize,
    NSApp,
    NSApplication,
    NSSecureTextField,
    NSKeyDown,
    NSCommandKeyMask,
    NSShiftKeyMask,
    NSControlKeyMask,
    NSDeviceIndependentModifierFlagsMask,
    NSSearchField,
    NSURL,
    NSDatePicker,
    NSTimeZone,
    NSBox,
)
import httpx
import objc
import datetime
import os

from symbols import SFSymbol
from utils import parse_color, check_if_installed
from constants import Orientation, MapType, convert_orientation, convert_map_type
from core.delegate import StackAppDelegate
from typing import Union

# Import SpriteKit for line chart
try:
    import SpriteKit

    SPRITEKIT_AVAILABLE = True
except ImportError:
    SPRITEKIT_AVAILABLE = False
    check_if_installed("SpriteKit")

# Import AVKit for video playback
try:
    import AVKit
    import AVFoundation

    AVKIT_AVAILABLE = True
except ImportError:
    AVKIT_AVAILABLE = False
    check_if_installed("AVKit")

# Import MapKit for maps
try:
    import MapKit

    MAPKIT_AVAILABLE = True
except ImportError:
    MAPKIT_AVAILABLE = False
    check_if_installed("MapKit")

# Import WebKit for web views
try:
    import WebKit

    WEBKIT_AVAILABLE = True
except ImportError:
    WEBKIT_AVAILABLE = False
    check_if_installed("WebKit")

# Global registry to keep delegate references alive
_delegate_registry = {}


class PersistentDefaultButton(NSButton):
    """NSButton subclass that maintains its default (blue) appearance.

    This prevents the button from losing its accent color when menus close/reopen
    or when other controls are interacted with.
    """

    def init(self):
        self = objc.super(PersistentDefaultButton, self).init()
        if self:
            self._should_maintain_key_equivalent = False
        return self

    @objc.python_method
    def set_persistent_key_equivalent(self, value):
        """Mark this button to maintain its key equivalent state."""
        self._should_maintain_key_equivalent = value
        if value:
            self.setKeyEquivalent_("\r")

    def resignFirstResponder(self):
        """Override to maintain key equivalent status even when resigning first responder."""
        result = objc.super(PersistentDefaultButton, self).resignFirstResponder()
        # restore key equivalent if we're supposed to maintain it
        if (
            hasattr(self, "_should_maintain_key_equivalent")
            and self._should_maintain_key_equivalent
        ):
            self.setKeyEquivalent_("\r")
        return result


class ScrollViewWithTextView(NSScrollView):
    def initWithSize_VScroll_(self, size: tuple[float, float], vscroll: bool):
        self = objc.super(ScrollViewWithTextView, self).initWithFrame_(
            NSMakeRect(0, 0, *size)
        )
        if not self:
            return
        self.setBorderType_(AppKit.NSBezelBorder)
        self.setHasVerticalScroller_(vscroll)
        self.setDrawsBackground_(True)
        self.setAutohidesScrollers_(True)
        self.setAutoresizingMask_(
            AppKit.NSViewWidthSizable | AppKit.NSViewHeightSizable
        )
        self.setTranslatesAutoresizingMaskIntoConstraints_(False)

        width_constraint = self.widthAnchor().constraintEqualToConstant_(size[0])
        width_constraint.setActive_(True)
        height_constraint = self.heightAnchor().constraintEqualToConstant_(size[1])
        height_constraint.setActive_(True)

        contentSize = self.contentSize()
        self.textView = NSTextView.alloc().initWithFrame_(self.contentView().frame())
        self.textView.setMinSize_(NSMakeSize(0.0, contentSize.height))
        self.textView.setMaxSize_(NSMakeSize(float("inf"), float("inf")))
        self.textView.setVerticallyResizable_(True)
        self.textView.setHorizontallyResizable_(False)
        self.setDocumentView_(self.textView)

        return self

    # provide access to some of the text view's methods
    def string(self):
        return self.textView.string()

    def setString_(self, text: str):
        self.textView.setString_(text)

    def setEditable_(self, editable: bool):
        self.textView.setEditable_(editable)

    def setSelectable_(self, selectable: bool):
        self.textView.setSelectable_(selectable)

    def setFont_(self, font: AppKit.NSFont):
        self.textView.setFont_(font)

    def setTextColor_(self, color: AppKit.NSColor):
        self.textView.setTextColor_(color)

    def setBackgroundColor_(self, color: AppKit.NSColor):
        self.textView.setBackgroundColor_(color)

    def performKeyEquivalent_(self, event):
        """Handle keyboard shortcuts like Cmd+C, Cmd+V, etc."""
        # Forward key equivalents to the text view for proper copy/paste handling
        if self.textView.performKeyEquivalent_(event):
            return True
        return objc.super(ScrollViewWithTextView, self).performKeyEquivalent_(event)


def _perform_key_equivalent(self, event):
    """Enhanced key equivalent handling for text fields."""
    if event.type() == AppKit.NSKeyDown:
        modifiers = event.modifierFlags() & AppKit.NSDeviceIndependentModifierFlagsMask

        if modifiers == AppKit.NSCommandKeyMask:
            char = event.charactersIgnoringModifiers()
            if char == "v":
                if NSApp.sendAction_to_from_(b"paste:", None, self):
                    return True
            elif char == "c":
                if NSApp.sendAction_to_from_(b"copy:", None, self):
                    return True
            elif char == "x":
                if NSApp.sendAction_to_from_(b"cut:", None, self):
                    return True
            elif char == "a":
                if NSApp.sendAction_to_from_(b"selectAll:", None, self):
                    return True
            elif char == "z":
                if NSApp.sendAction_to_from_(b"undo:", None, self):
                    return True
        elif modifiers == (AppKit.NSCommandKeyMask | AppKit.NSShiftKeyMask):
            char = event.charactersIgnoringModifiers()
            if char == "z":
                if NSApp.sendAction_to_from_(b"redo:", None, self):
                    return True
    return False


# Apply enhanced key handling to text field classes
NSTextField.performKeyEquivalent_ = _perform_key_equivalent
NSSecureTextField.performKeyEquivalent_ = _perform_key_equivalent
NSSearchField.performKeyEquivalent_ = _perform_key_equivalent
