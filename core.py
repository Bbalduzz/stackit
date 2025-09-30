#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Core StackIt components - isolated StackMenuItem implementation.
"""

import Foundation
import AppKit
from Foundation import NSDate, NSTimer, NSRunLoop, NSDefaultRunLoopMode, NSLog, NSObject, NSMakeRect, NSMakeSize
from AppKit import (
    NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSAlert, NSView, NSStackView,
    NSButton, NSImageView, NSTextField, NSFont, NSColor, NSImage, NSApp
)
from .sfsymbol import SFSymbol
from .delegate import StackAppDelegate
from . import controls
from PyObjCTools import AppHelper
import objc
import os
import weakref
import traceback


# Global state for the application
_STACK_APP_INSTANCE = None
_TIMERS = weakref.WeakKeyDictionary()

class ClickableView(NSView):
    """Custom NSView that forwards clicks to our callback system."""

    def initWithMenuItem_(self, menuitem):
        self = objc.super(ClickableView, self).init()
        if self:
            self._menuitem = menuitem
            self.setTranslatesAutoresizingMaskIntoConstraints_(False)
        return self

    def mouseDown_(self, event):
        """Handle mouse down events and forward to delegate callback system."""
        if self._menuitem in StackAppDelegate._callback_registry:
            stack_item, callback = StackAppDelegate._callback_registry[self._menuitem]
            try:
                StackAppDelegate._execute_callback(stack_item, callback)
            except Exception as e:
                NSLog(f"Error in clickable view action: {e}")


class StackView(NSStackView):
    """Custom NSStackView with list-like methods for easy manipulation."""

    def initWithOrientation_(self, orientation):
        self = objc.super(StackView, self).init()
        if self:
            self.setOrientation_(orientation)
            self.setAlignment_(AppKit.NSLayoutAttributeLeading)
            self.setSpacing_(8.0)
            self.setTranslatesAutoresizingMaskIntoConstraints_(False)
        return self

    @objc.python_method
    def append(self, view):
        """Add view to the end of the stack."""
        self.addArrangedSubview_(view)

    @objc.python_method
    def extend(self, views):
        """Add multiple views to the stack."""
        for view in views:
            self.append(view)

    @objc.python_method
    def insert(self, index, view):
        """Insert view at the specified index."""
        self.insertArrangedSubview_atIndex_(view, index)

    @objc.python_method
    def remove(self, view):
        """Remove view from the stack."""
        self.removeArrangedSubview_(view)
        view.removeFromSuperview()

    @objc.python_method
    def clear(self):
        """Remove all views from the stack."""
        for view in list(self.arrangedSubviews()):
            self.remove(view)


class StackMenuItem(NSObject):
    """A MenuItem that contains a custom NSStackView for building complex layouts."""

    def __new__(cls, title, key_equivalent=None, callback=None):
        # Create the instance using Objective-C allocation
        instance = cls.alloc().init()
        # Initialize it
        instance._title = str(title) if title is not None else ""
        instance._callback = callback
        instance._menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            instance._title, "menuItemCallback:", ""
        )
        # Set target to our delegate class
        instance._menuitem.setTarget_(StackAppDelegate)

        # Register this menu item for callbacks
        if callback:
            StackAppDelegate.register_callback(instance._menuitem, instance, callback)
        if key_equivalent:
            instance._menuitem.setKeyEquivalent_(key_equivalent)

        instance._custom_view = None
        instance._root_stack = None
        instance._padding = (6.0, 12.0, 6.0, 12.0)  # top, leading, bottom, trailing

        return instance


    @objc.python_method
    def _setup_custom_view(self):
        """Initialize the custom view for this menu item if not already done."""
        if self._custom_view is None:
            # Use ClickableView if we have a callback, otherwise regular NSView
            if self._callback:
                self._custom_view = ClickableView.alloc().initWithMenuItem_(self._menuitem)
            else:
                self._custom_view = NSView.alloc().init()
                self._custom_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
            # Only set the custom view if we actually need it
            # This preserves normal menu item behavior until we add custom content

    @objc.python_method
    def set_root_stack(self, stack_view):
        """Set the root stack view for this menu item."""
        self._setup_custom_view()

        # Now we actually need the custom view, so set it on the menu item
        self._menuitem.setView_(self._custom_view)

        if self._root_stack:
            self._root_stack.removeFromSuperview()

        self._root_stack = stack_view
        self._custom_view.addSubview_(stack_view)

        # Add constraints with proper macOS menu item padding
        padding_top, padding_leading, padding_bottom, padding_trailing = self._padding

        stack_view.topAnchor().constraintEqualToAnchor_constant_(self._custom_view.topAnchor(), padding_top).setActive_(True)
        stack_view.bottomAnchor().constraintEqualToAnchor_constant_(self._custom_view.bottomAnchor(), -padding_bottom).setActive_(True)
        stack_view.leadingAnchor().constraintEqualToAnchor_constant_(self._custom_view.leadingAnchor(), padding_leading).setActive_(True)
        stack_view.trailingAnchor().constraintEqualToAnchor_constant_(self._custom_view.trailingAnchor(), -padding_trailing).setActive_(True)

    @objc.python_method
    def hstack(self, controls=None, alignment=None, spacing=8.0):
        """Create and return a horizontal stack view."""
        stack = StackView.alloc().initWithOrientation_(AppKit.NSUserInterfaceLayoutOrientationHorizontal)
        if alignment is not None:
            stack.setAlignment_(alignment)
        else:
            stack.setAlignment_(AppKit.NSLayoutAttributeCenterY)
        stack.setSpacing_(spacing)

        if controls:
            stack.extend(controls)

        return stack

    @objc.python_method
    def vstack(self, controls=None, alignment=None, spacing=8.0):
        """Create and return a vertical stack view."""
        stack = StackView.alloc().initWithOrientation_(AppKit.NSUserInterfaceLayoutOrientationVertical)
        if alignment is not None:
            stack.setAlignment_(alignment)
        else:
            stack.setAlignment_(AppKit.NSLayoutAttributeLeading)
        stack.setSpacing_(spacing)

        if controls:
            stack.extend(controls)

        return stack

    @objc.python_method
    def label(self, text, font_size=13, bold=False, color=None):
        """Create a text label."""
        return controls.label(text, font_size, bold, color)

    @objc.python_method
    def image(self, image_path, width=None, height=None, scaling=None):
        """Create an image view."""
        return controls.image(image_path, width, height, scaling)

    @objc.python_method
    def button(self, title, target=None, action=None):
        """Create a button."""
        return controls.button(title, target, action)

    @objc.python_method
    def spacer(self, priority=250):
        """Create a spacer view that expands to fill available space."""
        return controls.spacer(priority)

    @objc.python_method
    def progress_bar(self, value=0.0, indeterminate=False, dimensions=(200, 20), show_text=True, color=None):
        """Create a horizontal progress bar."""
        return controls.progress_bar(value, indeterminate, dimensions, show_text, color)

    @objc.python_method
    def circular_progress(self, value=0.0, indeterminate=False, dimensions=(40, 40), color=None, line_width=3.0):
        """Create a circular progress indicator."""
        return controls.circular_progress(value, indeterminate, dimensions, color, line_width)


    # Properties for compatibility
    @objc.python_method
    def title(self):
        return self._title

    @objc.python_method
    def set_title(self, title):
        self._title = str(title)
        self._menuitem.setTitle_(self._title)

    @objc.python_method
    def set_callback(self, callback):
        self._callback = callback

    @objc.python_method
    def menuitem(self):
        """Get the underlying NSMenuItem."""
        return self._menuitem

class _StackApp(NSObject):
    """Minimal statusbar application using only StackMenuItem."""

    def init(self):
        """Default initializer - use the class method constructors instead."""
        raise RuntimeError("Use StackApp(title=..., icon=...) constructor instead")

    def initWithTitle_icon_(self, title=None, icon=None):
        """Internal initializer - use public constructor instead."""
        self = objc.super(_StackApp, self).init()
        if self:
            # Validate that at least one of title or icon is provided and not None
            if (title is None or title == "") and icon is None:
                raise ValueError("At least one of 'title' or 'icon' must be provided")

            global _STACK_APP_INSTANCE
            _STACK_APP_INSTANCE = self

            self._title = str(title) if title is not None else ""
            self._icon = icon
            self._menu_items = {}
            self._template = True

            # Initialize NSApplication first
            self._init_application()

            # Create and set up the delegate
            self._delegate = StackAppDelegate.alloc().initWithStackApp_(self)

            # Create menu
            self._menu = NSMenu.alloc().init()

            # Flag to track if default items have been added
            self._default_items_added = False

        return self

    @classmethod
    def stackApp(cls, title=None, icon=None):
        """Create a StackApp with modern API.

        Args:
            title: Optional title string for the status bar
            icon: Optional icon (Image, SFSymbol, or path string)

        At least one of title or icon must be provided.
        """
        return cls.alloc().initWithTitle_icon_(title, icon)

    @classmethod
    def stackAppWithTitle_icon_(cls, title, icon=None):
        """Factory method to create a StackApp (legacy compatibility)."""
        return cls.alloc().initWithTitle_icon_(title, icon)

    @objc.python_method
    def _add_default_menu_items(self):
        """Add default separator and Quit button to the menu."""
        # Add separator
        self.add_separator()

        # Create and add Quit button with ⌘Q shortcut
        quit_item = StackMenuItem("Quit", callback=self._default_quit_callback, key_equivalent="q")
        self.add_item("_quit", quit_item)

    @objc.python_method
    def _ensure_default_items(self):
        """Ensure default items (separator and Quit) are added at the bottom."""
        if not self._default_items_added:
            self._add_default_menu_items()
            self._default_items_added = True

    @objc.python_method
    def _default_quit_callback(self, sender):
        """Default quit callback that terminates the application."""
        NSApplication.sharedApplication().terminate_(None)

    @objc.python_method
    def _init_application(self):
        """Initialize NSApplication if not already done."""
        # This ensures NSApplication is properly initialized before creating GUI objects
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)

    @objc.python_method
    def add_item(self, key, stack_item):
        """Add a StackMenuItem to the menu."""
        if isinstance(stack_item, StackMenuItem):
            self._menu_items[key] = stack_item
            self._menu.addItem_(stack_item.menuitem())
        else:
            raise ValueError("Only StackMenuItem instances can be added")

    @objc.python_method
    def add_separator(self):
        """Add a separator to the menu."""
        self._menu.addItem_(NSMenuItem.separatorItem())

    @objc.python_method
    def remove_item(self, key):
        """Remove a menu item."""
        if key in self._menu_items:
            item = self._menu_items[key]
            self._menu.removeItem_(item.menuitem())
            del self._menu_items[key]

    @objc.python_method
    def get_item(self, key):
        """Get a menu item by key."""
        return self._menu_items.get(key)


    @objc.python_method
    def run(self):
        """Start the application run loop."""
        # Ensure default items are added at the end before running
        self._ensure_default_items()

        # Get the already initialized NSApplication
        nsapplication = NSApplication.sharedApplication()
        nsapplication.activateIgnoringOtherApps_(True)

        # Set up our custom delegate
        nsapplication.setDelegate_(self._delegate)

        # Install interrupt handler and run
        AppHelper.installMachInterrupt()
        AppHelper.runEventLoop()

    # Public API methods
    @objc.python_method
    def set_title(self, title):
        """Set the status bar title."""
        self._title = str(title)
        if self._delegate:
            self._delegate.set_title(title)

    @objc.python_method
    def set_icon(self, icon, template=True):
        """Set the status bar icon."""
        self._icon = icon
        self._template = template
        if self._delegate:
            self._delegate.set_icon(icon, template)

    @objc.python_method
    def show_menu(self):
        """Programmatically show the menu."""
        if self._delegate:
            self._delegate.show_menu()


class StackApp(_StackApp):
    """StackApp with modern Python constructor API and inheritance support.

    This class can be instantiated directly or subclassed:

    Direct usage:
        app = StackApp(title="My App")

    Subclassing:
        class MyApp(StackApp):
            def __init__(self):
                super().__init__(title="My App")
                # Your custom initialization
                self.setup_menu()
    """

    def __new__(cls, title=None, icon=None, **kwargs):
        """Create instance using Objective-C allocation."""
        # Allocate the instance of the correct class
        instance = cls.alloc()
        return instance

    def __init__(self, title=None, icon=None):
        """Initialize a StackApp with modern Python API.

        Args:
            title: Optional title string for the status bar
            icon: Optional icon (NSImage, SFSymbol, or path string)

        At least one of title or icon must be provided.
        The app automatically includes a separator and Quit button.

        Example:
            # With title only
            app = StackApp(title="My App")

            # With icon only
            app = StackApp(icon="gear")

            # With both
            app = StackApp(title="My App", icon=SFSymbol("gear"))
        """
        # Initialize using the Objective-C init method
        objc.super(StackApp, self).initWithTitle_icon_(title, icon)

