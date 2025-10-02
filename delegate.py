#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
StackBar Application Delegate

Provides a clean NSApplication delegate similar to rumps NSApp for handling
application lifecycle, callbacks, and system integration.
"""

import Foundation
import AppKit
from Foundation import NSLog, NSObject, NSWorkspace
from AppKit import NSApplication, NSStatusBar
from PyObjCTools import AppHelper
import objc
import traceback


class StackAppDelegate(NSObject):
    """NSApplication delegate for StackBar applications.

    Handles application lifecycle, callbacks, and system integration
    similar to rumps NSApp but for the isolated stackbar framework.
    """

    # Class-level callback registry (similar to rumps _ns_to_py_and_callback)
    _callback_registry = {}

    def initWithStackApp_(self, stack_app):
        """Initialize delegate with reference to StackApp instance."""
        self = objc.super(StackAppDelegate, self).init()
        if self:
            self._stack_app = stack_app
            self._status_item = None
            self._workspace_notifications_enabled = False
        return self

    # Application Lifecycle Methods
    def applicationDidFinishLaunching_(self, notification):
        """Called when the application finishes launching."""
        NSLog("StackBar application did finish launching")

        # Set up workspace notifications for sleep/wake events
        self._setup_workspace_notifications()

        # Initialize status bar
        self._initialize_status_bar()

        # Emit custom event if StackApp wants to handle it
        if hasattr(self._stack_app, '_on_ready'):
            try:
                self._stack_app._on_ready()
            except Exception as e:
                NSLog(f"Error in StackApp ready callback: {e}")

    def applicationWillTerminate_(self, notification):
        """Called when application is about to terminate."""
        NSLog("StackBar application will terminate")

        # Clean up workspace notifications
        self._cleanup_workspace_notifications()

        # Emit custom event if StackApp wants to handle it
        if hasattr(self._stack_app, '_on_quit'):
            try:
                self._stack_app._on_quit()
            except Exception as e:
                NSLog(f"Error in StackApp quit callback: {e}")

    def applicationShouldTerminate_(self, sender):
        """Determine if application should terminate."""
        return AppKit.NSTerminateNow

    # Status Bar Management
    def _initialize_status_bar(self):
        """Initialize the status bar item."""
        if not self._status_item and self._stack_app:
            status_bar = NSStatusBar.systemStatusBar()
            self._status_item = status_bar.statusItemWithLength_(AppKit.NSVariableStatusItemLength)

            # Set title and icon from StackApp
            self._update_status_bar_appearance()

            # Set menu
            if hasattr(self._stack_app, '_menu'):
                self._status_item.setMenu_(self._stack_app._menu)

    def _update_status_bar_appearance(self):
        """Update status bar title and icon."""
        if not self._status_item or not self._stack_app:
            return

        # Set icon if available
        if hasattr(self._stack_app, '_icon') and self._stack_app._icon:
            try:
                from .sfsymbol import SFSymbol
                image = None

                # Handle SFSymbol objects
                is_sfsymbol = False
                sfsymbol_rendering = None

                if isinstance(self._stack_app._icon, SFSymbol):
                    image = self._stack_app._icon._nsimage
                    is_sfsymbol = True
                    sfsymbol_rendering = self._stack_app._icon.rendering
                # Handle NSImage objects
                elif hasattr(self._stack_app._icon, 'setTemplate_'):
                    image = self._stack_app._icon
                # Handle string paths or SF Symbol names
                else:
                    import os
                    icon_path = str(self._stack_app._icon)
                    if os.path.exists(icon_path):
                        image = AppKit.NSImage.alloc().initByReferencingFile_(icon_path)
                    else:
                        # Try as SF Symbol name
                        try:
                            sf_symbol = SFSymbol(icon_path)
                            image = sf_symbol._nsimage
                            is_sfsymbol = True
                            sfsymbol_rendering = sf_symbol.rendering
                        except:
                            # Try as named system image
                            image = AppKit.NSImage.imageNamed_(icon_path)

                if image:
                    # Only set template mode if it's not an SFSymbol with special rendering
                    # Template mode forces monochrome, which overrides SF Symbol rendering modes
                    should_set_template = hasattr(self._stack_app, '_template') and self._stack_app._template
                    if is_sfsymbol and sfsymbol_rendering not in ["automatic", "monochrome", None]:
                        # Don't set template for multicolor, hierarchical, or palette rendering
                        should_set_template = False

                    if should_set_template:
                        image.setTemplate_(True)

                    self._status_item.button().setImage_(image)
                    # Also set title if available (supports both icon and title)
                    if hasattr(self._stack_app, '_title') and self._stack_app._title:
                        self._status_item.button().setTitle_(self._stack_app._title)
                    else:
                        self._status_item.button().setTitle_("")
                else:
                    # Fall back to title
                    self._set_status_bar_title()
            except Exception as e:
                NSLog(f"Error setting status bar icon: {e}")
                self._set_status_bar_title()
        else:
            self._set_status_bar_title()

    def _set_status_bar_title(self):
        """Set status bar title."""
        if self._status_item and self._stack_app:
            title = getattr(self._stack_app, '_title', 'StackBar App')
            self._status_item.button().setTitle_(title)

    # Workspace Notifications (Sleep/Wake)
    def _setup_workspace_notifications(self):
        """Set up workspace notifications for sleep/wake events."""
        if not self._workspace_notifications_enabled:
            workspace = NSWorkspace.sharedWorkspace()
            notification_center = workspace.notificationCenter()

            notification_center.addObserver_selector_name_object_(
                self,
                "receiveSleepNotification:",
                "NSWorkspaceWillSleepNotification",
                None
            )

            notification_center.addObserver_selector_name_object_(
                self,
                "receiveWakeNotification:",
                "NSWorkspaceDidWakeNotification",
                None
            )

            self._workspace_notifications_enabled = True

    def _cleanup_workspace_notifications(self):
        """Clean up workspace notifications."""
        if self._workspace_notifications_enabled:
            workspace = NSWorkspace.sharedWorkspace()
            notification_center = workspace.notificationCenter()
            notification_center.removeObserver_(self)
            self._workspace_notifications_enabled = False

    def receiveSleepNotification_(self, notification):
        """Handle system sleep notification."""
        NSLog("System going to sleep")
        if hasattr(self._stack_app, '_on_sleep'):
            try:
                self._stack_app._on_sleep()
            except Exception as e:
                NSLog(f"Error in sleep callback: {e}")

    def receiveWakeNotification_(self, notification):
        """Handle system wake notification."""
        NSLog("System waking up")
        if hasattr(self._stack_app, '_on_wake'):
            try:
                self._stack_app._on_wake()
            except Exception as e:
                NSLog(f"Error in wake callback: {e}")

    # Centralized Callback Management
    @classmethod
    def register_callback(cls, obj, stack_item, callback):
        """Register a callback for an NSObject (menu item, button, etc).

        Args:
            obj: NSObject that will trigger the callback
            stack_item: StackMenuItem instance
            callback: Callback function or method name
        """
        cls._callback_registry[obj] = (stack_item, callback)

    @classmethod
    def unregister_callback(cls, obj):
        """Unregister a callback for an NSObject."""
        if obj in cls._callback_registry:
            del cls._callback_registry[obj]

    @classmethod
    def menuItemCallback_(cls, sender):
        """Handle menu item callbacks."""
        if sender in cls._callback_registry:
            stack_item, callback = cls._callback_registry[sender]
            try:
                cls._execute_callback(stack_item, callback)
            except Exception as e:
                NSLog(f"Error in menu item callback: {e}")
                traceback.print_exc()

    @classmethod
    def buttonCallback_(cls, sender):
        """Handle button callbacks."""
        if sender in cls._callback_registry:
            stack_item, callback = cls._callback_registry[sender]
            try:
                cls._execute_callback(stack_item, callback)
            except Exception as e:
                NSLog(f"Error in button callback: {e}")
                traceback.print_exc()

    @classmethod
    def sliderCallback_(cls, sender):
        """Handle slider callbacks."""
        print(f"🎛️ Slider callback triggered! Value: {sender.doubleValue()}")
        if sender in cls._callback_registry:
            stack_item, callback = cls._callback_registry[sender]
            try:
                # For controls, we pass the sender (NSSlider) to the callback
                if callable(callback):
                    callback(sender)
                elif isinstance(callback, str):
                    # Handle string callbacks if needed
                    cls._execute_callback(stack_item, callback)
            except Exception as e:
                NSLog(f"Error in slider callback: {e}")
                traceback.print_exc()
        else:
            print(f"❌ Slider {sender} not found in callback registry")

    @classmethod
    def checkboxCallback_(cls, sender):
        """Handle checkbox callbacks."""
        print(f"☑️ Checkbox callback triggered! State: {sender.state()}")
        if sender in cls._callback_registry:
            stack_item, callback = cls._callback_registry[sender]
            try:
                if callable(callback):
                    callback(sender)
                elif isinstance(callback, str):
                    cls._execute_callback(stack_item, callback)
            except Exception as e:
                NSLog(f"Error in checkbox callback: {e}")
                traceback.print_exc()
        else:
            print(f"❌ Checkbox {sender} not found in callback registry")

    @classmethod
    def comboboxCallback_(cls, sender):
        """Handle combobox selection callbacks."""
        print(f"📋 Combobox callback triggered! Index: {sender.indexOfSelectedItem()}")
        if sender in cls._callback_registry:
            stack_item, callback = cls._callback_registry[sender]
            try:
                if callable(callback):
                    callback(sender)
                elif isinstance(callback, str):
                    cls._execute_callback(stack_item, callback)
            except Exception as e:
                NSLog(f"Error in combobox callback: {e}")
                traceback.print_exc()
        else:
            print(f"❌ Combobox {sender} not found in callback registry")

    @classmethod
    def searchFieldCallback_(cls, sender):
        """Handle search field callbacks."""
        print(f"🔍 Search field callback triggered! Text: {sender.stringValue()}")
        if sender in cls._callback_registry:
            stack_item, callback = cls._callback_registry[sender]
            try:
                if callable(callback):
                    callback(sender)
                elif isinstance(callback, str):
                    cls._execute_callback(stack_item, callback)
            except Exception as e:
                NSLog(f"Error in search field callback: {e}")
                traceback.print_exc()

    @classmethod
    def datePickerCallback_(cls, sender):
        """Handle date picker callbacks."""
        print(f"📅 Date picker callback triggered! Date: {sender.dateValue()}")
        if sender in cls._callback_registry:
            stack_item, callback = cls._callback_registry[sender]
            try:
                if callable(callback):
                    callback(sender)
                elif isinstance(callback, str):
                    cls._execute_callback(stack_item, callback)
            except Exception as e:
                NSLog(f"Error in date picker callback: {e}")
                traceback.print_exc()

    @classmethod
    def radioButtonCallback_(cls, sender):
        """Handle radio button callbacks."""
        print(f"🔘 Radio button callback triggered! State: {sender.state()}")
        if sender in cls._callback_registry:
            stack_item, callback = cls._callback_registry[sender]
            try:
                if callable(callback):
                    callback(sender)
                elif isinstance(callback, str):
                    cls._execute_callback(stack_item, callback)
            except Exception as e:
                NSLog(f"Error in radio button callback: {e}")
                traceback.print_exc()

    @classmethod
    def _execute_callback(cls, stack_item, callback):
        """Execute a callback with proper error handling."""
        if callable(callback):
            callback(stack_item)
        elif isinstance(callback, str):
            # Try to find method on stack_item first, then on app instance
            if hasattr(stack_item, callback):
                method = getattr(stack_item, callback)
                method(stack_item)
            else:
                # Try to find on app instance
                # We need to get the app instance somehow - could store it globally
                from .core import _STACK_APP_INSTANCE
                if _STACK_APP_INSTANCE and hasattr(_STACK_APP_INSTANCE, callback):
                    method = getattr(_STACK_APP_INSTANCE, callback)
                    method(stack_item)
                else:
                    NSLog(f"Callback method '{callback}' not found")
        else:
            NSLog(f"Invalid callback type: {type(callback)}")

    # Public API Methods
    def set_title(self, title):
        """Set the status bar title."""
        if self._stack_app:
            self._stack_app._title = str(title)
            self._set_status_bar_title()

    def set_icon(self, icon, template=True):
        """Set the status bar icon."""
        if self._stack_app:
            self._stack_app._icon = icon
            self._stack_app._template = template
            self._update_status_bar_appearance()

    def show_menu(self):
        """Programmatically show the menu."""
        if self._status_item:
            self._status_item.button().performClick_(None)

    # Menu Delegate Methods (NSMenuDelegate)
    def menuWillOpen_(self, menu):
        """Called when menu is about to open."""
        # Keep menu responsive by ensuring it remains key
        pass

    def menuDidClose_(self, menu):
        """Called when menu closes."""
        # Release any first responders when menu closes
        NSApplication.sharedApplication().keyWindow().makeFirstResponder_(None)

    def confinementRectForMenu_onScreen_(self, menu, screen):
        """Return the confinement rect for the menu.

        This helps prevent the menu from moving when controls are interacted with.
        """
        return screen.visibleFrame() if screen else AppKit.NSZeroRect