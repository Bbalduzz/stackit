#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Core StackIt components - isolated StackMenuItem implementation.
"""

import Foundation
import AppKit
from Foundation import (
    NSDate,
    NSTimer,
    NSRunLoop,
    NSDefaultRunLoopMode,
    NSLog,
    NSObject,
    NSMakeRect,
    NSMakeSize,
)
from AppKit import (
    NSApplication,
    NSStatusBar,
    NSMenu,
    NSMenuItem,
    NSAlert,
    NSView,
    NSStackView,
    NSButton,
    NSImageView,
    NSTextField,
    NSFont,
    NSColor,
    NSImage,
    NSApp,
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
    """Custom NSView that forwards clicks to our callback system and manages focus properly."""

    def initWithMenuItem_(self, menuitem):
        self = objc.super(ClickableView, self).init()
        if self:
            self._menuitem = menuitem
            self.setTranslatesAutoresizingMaskIntoConstraints_(False)
        return self

    def acceptsFirstResponder(self):
        """Prevent this view from becoming first responder to keep menu responsive."""
        return False

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


# Standalone layout functions
def hstack(controls=None, alignment=None, spacing=8.0):
    """Create a horizontal stack view.

    Args:
        controls: Optional list of controls to add to the stack
        alignment: Optional alignment (NSLayoutAttribute constant)
        spacing: Spacing between controls in points (default: 8.0)

    Returns:
        StackView configured for horizontal layout
    """
    alignments_map = {
        "center_x": AppKit.NSLayoutAttributeCenterX,
        "center_y": AppKit.NSLayoutAttributeCenterY,
        "leading": AppKit.NSLayoutAttributeLeading,
        "trailing": AppKit.NSLayoutAttributeTrailing,
    }
    stack = StackView.alloc().initWithOrientation_(
        AppKit.NSUserInterfaceLayoutOrientationHorizontal
    )
    if alignment is not None:
        stack.setAlignment_(alignments_map[alignment])
    else:
        stack.setAlignment_(AppKit.NSLayoutAttributeCenterY)
    stack.setSpacing_(spacing)

    if controls:
        stack.extend(controls)

    return stack


class ResponsiveMenu(NSMenu):
    """Custom NSMenu that maintains keyboard responsiveness even when controls have focus."""

    def performKeyEquivalent_(self, event):
        """Handle keyboard events even when menu items have focused controls."""
        # Try the standard menu key equivalent handling first
        if objc.super(ResponsiveMenu, self).performKeyEquivalent_(event):
            return True

        # If that didn't work and a control has focus, ensure key equivalents still work
        # by checking all menu items manually
        modifiers = event.modifierFlags()
        characters = event.charactersIgnoringModifiers()

        if characters and (modifiers & AppKit.NSEventModifierFlagCommand):
            # Walk through menu items and check for matching key equivalents
            for item in self.itemArray():
                if item.keyEquivalent() == characters:
                    # Found a match, perform the action
                    if item.target() and item.action():
                        NSApplication.sharedApplication().sendAction_to_from_(
                            item.action(), item.target(), self
                        )
                        return True
        return False


def vstack(controls=None, alignment=None, spacing=8.0):
    """Create a vertical stack view.

    Args:
        controls: Optional list of controls to add to the stack
        alignment: Optional alignment (NSLayoutAttribute constant)
        spacing: Spacing between controls in points (default: 8.0)

    Returns:
        StackView configured for vertical layout
    """
    stack = StackView.alloc().initWithOrientation_(
        AppKit.NSUserInterfaceLayoutOrientationVertical
    )
    if alignment is not None:
        stack.setAlignment_(alignment)
    else:
        stack.setAlignment_(AppKit.NSLayoutAttributeLeading)
    stack.setSpacing_(spacing)

    if controls:
        stack.extend(controls)

    return stack


class MenuItem(NSObject):
    """A MenuItem that can be either simple (title-based) or custom (layout-based).

    Simple menu items:
        MenuItem(title="Preferences", callback=my_func, key_equivalent=",")

    Custom layout menu items:
        MenuItem(layout=stackit.hstack([...]))

    Menu items with submenus:
        MenuItem(title="Settings", submenu=[MenuItem(...), MenuItem(...)])
    """

    def __new__(
        cls,
        title=None,
        layout=None,
        callback=None,
        key_equivalent=None,
        submenu=None,
        badge=None,
    ):
        # Create the instance using Objective-C allocation
        instance = cls.alloc().init()
        # Initialize it
        instance._callback = callback
        instance._title = str(title) if title else ""
        instance._menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            instance._title, "menuItemCallback:", ""
        )
        # Set target to our delegate class
        instance._menuitem.setTarget_(StackAppDelegate)

        # Register this menu item for callbacks (only if no submenu)
        if callback and submenu is None:
            StackAppDelegate.register_callback(instance._menuitem, instance, callback)
        if key_equivalent:
            instance._menuitem.setKeyEquivalent_(key_equivalent)

        instance._custom_view = None
        instance._root_stack = None
        instance._padding = (6.0, 12.0, 6.0, 12.0)  # top, leading, bottom, trailing
        instance._is_simple = title is not None and layout is None
        instance._submenu = None
        instance._badge = None

        # Set layout if provided (only for custom menu items)
        if layout is not None:
            instance.set_layout(layout)

        # Set submenu if provided
        if submenu is not None:
            instance.set_submenu(submenu)

        # Set badge if provided (macOS 14.0+)
        if badge is not None:
            instance.set_badge(badge)

        return instance

    @objc.python_method
    def _setup_custom_view(self):
        """Initialize the custom view for this menu item if not already done."""
        if self._custom_view is None:
            # Use ClickableView if we have a callback, otherwise regular NSView
            if self._callback:
                self._custom_view = ClickableView.alloc().initWithMenuItem_(
                    self._menuitem
                )
            else:
                self._custom_view = NSView.alloc().init()
                self._custom_view.setTranslatesAutoresizingMaskIntoConstraints_(False)

    @objc.python_method
    def set_layout(self, stack_view):
        """Set the layout for this menu item."""
        self._setup_custom_view()

        # Now we actually need the custom view, so set it on the menu item
        self._menuitem.setView_(self._custom_view)

        if self._root_stack:
            self._root_stack.removeFromSuperview()

        self._root_stack = stack_view
        self._custom_view.addSubview_(stack_view)

        # Add constraints with proper macOS menu item padding
        padding_top, padding_leading, padding_bottom, padding_trailing = self._padding

        stack_view.topAnchor().constraintEqualToAnchor_constant_(
            self._custom_view.topAnchor(), padding_top
        ).setActive_(True)
        stack_view.bottomAnchor().constraintEqualToAnchor_constant_(
            self._custom_view.bottomAnchor(), -padding_bottom
        ).setActive_(True)
        stack_view.leadingAnchor().constraintEqualToAnchor_constant_(
            self._custom_view.leadingAnchor(), padding_leading
        ).setActive_(True)
        stack_view.trailingAnchor().constraintEqualToAnchor_constant_(
            self._custom_view.trailingAnchor(), -padding_trailing
        ).setActive_(True)

        # Force the view to update its layout and redraw
        self._custom_view.setNeedsLayout_(True)
        self._custom_view.setNeedsDisplay_(True)
        if hasattr(self._custom_view, "layoutSubtreeIfNeeded"):
            self._custom_view.layoutSubtreeIfNeeded()

    @objc.python_method
    def set_callback(self, callback):
        """Set or update the callback for this menu item."""
        self._callback = callback
        if callback:
            StackAppDelegate.register_callback(self._menuitem, self, callback)

    @objc.python_method
    def set_submenu(self, items):
        """Set a submenu for this menu item.

        Args:
            items: List of MenuItem objects or 'separator' strings

        Example:
            submenu_items = [
                MenuItem(title="Option 1", callback=func1),
                'separator',
                MenuItem(title="Option 2", callback=func2)
            ]
            item.set_submenu(submenu_items)
        """
        # Create a new responsive menu for the submenu
        submenu = ResponsiveMenu.alloc().init()
        submenu.setAutoenablesItems_(False)

        # Add items to submenu
        for item in items:
            if isinstance(item, str) and item.lower() == "separator":
                submenu.addItem_(NSMenuItem.separatorItem())
            elif isinstance(item, MenuItem):
                submenu.addItem_(item._menuitem)
            else:
                NSLog(f"Warning: Invalid submenu item type: {type(item)}")

        # Attach submenu to this menu item
        self._menuitem.setSubmenu_(submenu)
        self._submenu = submenu

    @objc.python_method
    def set_badge(self, badge_type, count=None):
        """Set a badge for this menu item (macOS 14.0+).

        Args:
            badge_type: String indicating badge type
                       Supported types: "updates", "new-items", "alerts", or None to remove
            count: Optional badge count (integer). If None, uses system default.

        Example:
            item.set_badge("updates")           # Shows "updates available" badge
            item.set_badge("updates", count=5)  # Shows badge with count 5
            item.set_badge("new-items")         # Shows "new items" badge
            item.set_badge("alerts")            # Shows "alerts" badge
            item.set_badge(None)                # Removes badge
        """
        # Check if NSMenuItemBadge is available (macOS 14.0+)
        if not hasattr(AppKit, "NSMenuItemBadge"):
            NSLog("Warning: NSMenuItemBadge requires macOS 14.0 or later")
            return

        try:
            # Remove badge if None
            if badge_type is None:
                self._menuitem.setBadge_(None)
                self._badge = None
                return

            # Map badge type string to NSMenuItemBadgeType constant
            if isinstance(badge_type, str):
                badge_type_lower = badge_type.lower().replace("-", "").replace("_", "")

                if badge_type_lower in ["updates", "update"]:
                    badge_type_enum = AppKit.NSMenuItemBadgeTypeUpdates
                elif badge_type_lower in ["newitems", "new"]:
                    badge_type_enum = AppKit.NSMenuItemBadgeTypeNewItems
                elif badge_type_lower in ["alerts", "alert"]:
                    badge_type_enum = AppKit.NSMenuItemBadgeTypeAlerts
                else:
                    NSLog(
                        f"Warning: Unknown badge type '{badge_type}'. Use 'updates', 'new-items', or 'alerts'"
                    )
                    return
            else:
                # Assume it's already a badge type constant
                badge_type_enum = badge_type

            # Create badge with count if specified, otherwise use type-only initializer
            if count is not None:
                badge = AppKit.NSMenuItemBadge.alloc().initWithCount_type_(
                    count, badge_type_enum
                )
            else:
                # Use count 0 for default badge appearance (no number shown)
                badge = AppKit.NSMenuItemBadge.alloc().initWithCount_type_(
                    0, badge_type_enum
                )

            # Set the badge on the menu item
            if hasattr(self._menuitem, "setBadge_"):
                self._menuitem.setBadge_(badge)
                self._badge = badge
            else:
                NSLog("Warning: setBadge_ not available on NSMenuItem")
        except Exception as e:
            NSLog(f"Error setting badge: {e}")

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

            # Create menu with responsive keyboard handling
            self._menu = ResponsiveMenu.alloc().init()
            self._menu.setAutoenablesItems_(False)
            self._menu.setDelegate_(self._delegate)

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

        # Create and add Quit button with ⌘Q shortcut (simple menu item)
        quit_item = MenuItem(
            title="Quit", callback=self._default_quit_callback, key_equivalent="q"
        )
        self.add(quit_item)

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
    def add(self, menu_item, key=None):
        """Add a MenuItem to the menu.

        Args:
            menu_item: MenuItem instance to add
            key: Optional key for later reference (auto-generated if not provided)
        """
        if not isinstance(menu_item, MenuItem):
            raise ValueError("Only MenuItem instances can be added")

        # Auto-generate key if not provided
        if key is None:
            key = f"_item_{len(self._menu_items)}"

        self._menu_items[key] = menu_item
        self._menu.addItem_(menu_item.menuitem())

        return key  # Return key for reference if needed

    @objc.python_method
    def add_separator(self):
        """Add a separator to the menu."""
        self._menu.addItem_(NSMenuItem.separatorItem())

    @objc.python_method
    def remove(self, key):
        """Remove a menu item by key.

        Args:
            key: Key of the menu item to remove
        """
        if key in self._menu_items:
            item = self._menu_items[key]
            self._menu.removeItem_(item.menuitem())
            del self._menu_items[key]

    @objc.python_method
    def get(self, key):
        """Get a menu item by key.

        Args:
            key: Key of the menu item to retrieve

        Returns:
            MenuItem instance or None if not found
        """
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

    @objc.python_method
    def update(self):
        """Force the menu to update and redraw.

        Call this method after updating menu item layouts to ensure
        changes are visible even when the menu is open.
        """
        # Force all menu items to update their views
        for menu_item in self._menu_items.values():
            if menu_item._custom_view:
                menu_item._custom_view.setNeedsLayout_(True)
                menu_item._custom_view.setNeedsDisplay_(True)

        # Update the menu itself
        self._menu.update()


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
