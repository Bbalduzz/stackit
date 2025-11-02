#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions for StackIt applications.
"""

import objc
import AppKit
from AppKit import NSAlert, NSApp, NSApplication, NSWorkspace, NSColor
from Foundation import (
    NSUserNotification,
    NSUserNotificationCenter,
    NSLog,
    NSTimer,
    NSRunLoop,
    NSDefaultRunLoopMode,
    NSRunLoopCommonModes,
)
import subprocess
import json
import os


def alert(title=None, message="", ok=None, cancel=None, icon_path=None):
    """Generate a simple alert window.

    Args:
        title: the text positioned at the top of the window in larger font
        message: the text positioned below the title in smaller font
        ok: the text for the "ok" button
        cancel: the text for the "cancel" button
        icon_path: a path to an image for the alert icon

    Returns:
        a number representing the button pressed (1 for ok, 0 for cancel)
    """
    message = str(message)
    message = message.replace("%", "%%")
    if title is not None:
        title = str(title)

    if not isinstance(cancel, str):
        cancel = "Cancel" if cancel else None

    alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
        title, ok, cancel, None, message
    )

    alert.setAlertStyle_(0)  # informational style

    if icon_path is not None:
        try:
            icon = AppKit.NSImage.alloc().initByReferencingFile_(str(icon_path))
            if icon:
                alert.setIcon_(icon)
        except:
            pass

    NSLog(f"alert opened with message: {repr(message)}, title: {repr(title)}")
    return alert.runModal()


def notification(title, subtitle=None, message=None, sound=True):
    """Send a system notification.

    Args:
        title: the notification title
        subtitle: optional subtitle
        message: optional message body
        sound: whether to play notification sound
    """
    try:
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(str(title))

        if subtitle:
            notification.setSubtitle_(str(subtitle))
        if message:
            notification.setInformativeText_(str(message))
        if sound:
            notification.setSoundName_("NSUserNotificationDefaultSoundName")

        center = NSUserNotificationCenter.defaultUserNotificationCenter()

        # Check if notification center is available (it may be None on newer macOS versions)
        if center is None:
            NSLog(f"NSUserNotificationCenter not available. Notification: {title}")
            # Fall back to console log
            if subtitle:
                NSLog(f"  Subtitle: {subtitle}")
            if message:
                NSLog(f"  Message: {message}")
            return

        center.deliverNotification_(notification)

    except Exception as e:
        NSLog(f"Error sending notification: {e}")


def quit_application(sender=None):
    """Quit the application. Some menu item should call this function so that the application can exit gracefully."""
    nsapplication = NSApplication.sharedApplication()
    nsapplication.terminate_(sender)


def open_url(url):
    """Open a URL in the default browser."""
    try:
        workspace = NSWorkspace.sharedWorkspace()
        workspace.openURL_(AppKit.NSURL.URLWithString_(str(url)))
    except Exception as e:
        NSLog(f"Error opening URL: {e}")


def choose_directory(title="Choose Directory", default_directory=None):
    """Open a directory picker dialog.

    Args:
        title: title of the picker dialog
        default_directory: optional default directory path

    Returns:
        selected directory path or None if cancelled
    """
    panel = AppKit.NSOpenPanel.openPanel()
    panel.setTitle_(title)
    panel.setCanChooseFiles_(False)
    panel.setCanChooseDirectories_(True)
    panel.setCanCreateDirectories_(True)
    panel.setAllowsMultipleSelection_(False)

    if default_directory:
        import os

        if os.path.exists(default_directory):
            url = AppKit.NSURL.fileURLWithPath_(default_directory)
            panel.setDirectoryURL_(url)

    result = panel.runModal()
    if result == AppKit.NSModalResponseOK:
        return panel.URL().path()
    return None


def run_command(command, timeout=30):
    """Run a shell command and return the result.

    Args:
        command: command to run (string or list)
        timeout: timeout in seconds

    Returns:
        tuple of (returncode, stdout, stderr)
    """
    try:
        if isinstance(command, str):
            command = command.split()

        result = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout
        )

        return result.returncode, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def get_application_support_path(app_name):
    """Get the application support directory for the app."""
    import os
    from Foundation import NSSearchPathForDirectoriesInDomains

    app_support_path = os.path.join(
        NSSearchPathForDirectoriesInDomains(14, 1, 1).objectAtIndex_(0), app_name
    )

    if not os.path.isdir(app_support_path):
        os.makedirs(app_support_path, exist_ok=True)

    return app_support_path


def save_preferences(app_name, preferences):
    """Save preferences to application support directory.

    Args:
        app_name: name of the application
        preferences: dictionary of preferences to save
    """
    import json
    import os

    try:
        app_support = get_application_support_path(app_name)
        prefs_path = os.path.join(app_support, "preferences.json")

        with open(prefs_path, "w") as f:
            json.dump(preferences, f, indent=2)

    except Exception as e:
        NSLog(f"Error saving preferences: {e}")


def load_preferences(app_name, defaults=None):
    """Load preferences from application support directory.

    Args:
        app_name: name of the application
        defaults: default preferences dictionary

    Returns:
        preferences dictionary
    """

    if defaults is None:
        defaults = {}

    try:
        app_support = get_application_support_path(app_name)
        prefs_path = os.path.join(app_support, "preferences.json")

        if os.path.exists(prefs_path):
            with open(prefs_path, "r") as f:
                return json.load(f)
        else:
            return defaults

    except Exception as e:
        NSLog(f"Error loading preferences: {e}")
        return defaults


class _TimerTarget(AppKit.NSObject):
    def initWithCallback_(self, cb):
        self = objc.super(_TimerTarget, self).init()
        if self:
            self.callback = cb
        return self

    def timerFired_(self, timer):
        if self.callback:
            try:
                self.callback(timer)
            except Exception as e:
                NSLog(f"Timer callback error: {e}")


class _TimerScheduler(AppKit.NSObject):
    """Helper class to schedule timers on the main thread."""

    def initWithInterval_callback_repeats_(self, interval, callback, repeats):
        self = objc.super(_TimerScheduler, self).init()
        if self:
            self.interval = interval
            self.callback = callback
            self.repeats = repeats
            self.timer_result = None
        return self

    def scheduleTimer(self):
        """Called on main thread to schedule the timer."""
        from Foundation import NSRunLoop

        target = _TimerTarget.alloc().initWithCallback_(self.callback)
        self.timer_result = (
            NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(
                self.interval, target, "timerFired:", None, self.repeats
            )
        )
        # Schedule on main run loop in common modes
        NSRunLoop.mainRunLoop().addTimer_forMode_(
            self.timer_result, NSRunLoopCommonModes
        )


def timer(interval, callback, repeats=True):
    """Create a timer that calls a function at regular intervals.

    This function is thread-safe and will automatically schedule the timer on
    the main thread's run loop, regardless of which thread it's called from.

    Args:
        interval: time interval in seconds
        callback: function to call
        repeats: whether the timer repeats

    Returns:
        NSTimer object
    """
    from Foundation import NSThread, NSRunLoop

    def schedule_timer():
        target = _TimerTarget.alloc().initWithCallback_(callback)
        timer_obj = NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(
            interval, target, "timerFired:", None, repeats
        )
        # Schedule on main run loop in common modes so it works even when menus are open
        NSRunLoop.mainRunLoop().addTimer_forMode_(timer_obj, NSRunLoopCommonModes)
        return timer_obj

    # If we're already on the main thread, schedule directly
    if NSThread.isMainThread():
        return schedule_timer()
    else:
        # If on background thread, schedule on main thread using helper
        scheduler = _TimerScheduler.alloc().initWithInterval_callback_repeats_(
            interval, callback, repeats
        )
        scheduler.performSelectorOnMainThread_withObject_waitUntilDone_(
            "scheduleTimer", None, True  # Wait until done to get the timer reference
        )
        return scheduler.timer_result


def after(seconds, callback):
    """Run a callback once after a delay.

    This function is thread-safe and can be called from any thread. The timer
    will be automatically scheduled on the main thread's run loop.

    Args:
        seconds: delay in seconds before running callback
        callback: function to call (receives timer as argument)

    Returns:
        NSTimer object

    Example:
        def delayed_action(timer):
            print("Executed after 2 seconds")

        stackit.after(2.0, delayed_action)

        # Can also be called from background threads
        def background_task():
            # Do some work...
            stackit.after(0.0, lambda timer: update_ui())  # Safe!
    """
    return timer(seconds, callback, repeats=False)


def every(seconds, callback):
    """Run a callback repeatedly at a fixed interval.

    This function is thread-safe and can be called from any thread. The timer
    will be automatically scheduled on the main thread's run loop.

    Args:
        seconds: interval in seconds between callback executions
        callback: function to call (receives timer as argument)

    Returns:
        NSTimer object (call timer.invalidate() to stop)

    Example:
        def periodic_check(timer):
            print("Called every 5 seconds")

        timer = stackit.every(5.0, periodic_check)
        # Later: timer.invalidate() to stop
    """
    return timer(seconds, callback, repeats=True)


def parse_color(color, default=None):
    """Parse a color from various formats into NSColor.

    Args:
        color: Color in various formats:
            - NSColor object (returned as-is)
            - Hex string: "#RRGGBB" or "#RRGGBBAA"
            - RGB tuple: (r, g, b) with values 0-255 or 0.0-1.0
            - RGBA tuple: (r, g, b, a) with values 0-255 or 0.0-1.0
        default: Default NSColor to return if parsing fails (default: NSColor.labelColor())

    Returns:
        NSColor object

    Example:
        parse_color("#FF0000")  # Red
        parse_color("#FF0000AA")  # Red with alpha
        parse_color((255, 0, 0))  # Red (0-255 range)
        parse_color((1.0, 0.0, 0.0))  # Red (0.0-1.0 range)
        parse_color((255, 0, 0, 128))  # Red with alpha
    """
    if default is None:
        default = NSColor.labelColor()

    # Already an NSColor
    if isinstance(color, NSColor):
        return color

    # Hex string
    if isinstance(color, str):
        if color.startswith("#"):
            hex_color = color[1:]
            try:
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
            except (ValueError, IndexError):
                return default
        return default

    # Tuple (RGB or RGBA)
    if isinstance(color, (tuple, list)):
        try:
            if len(color) == 3:
                r, g, b = color
                # Normalize 0-255 range to 0.0-1.0
                if r > 1.0 or g > 1.0 or b > 1.0:
                    r, g, b = r / 255.0, g / 255.0, b / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, 1.0)
            elif len(color) == 4:
                r, g, b, a = color
                # Normalize 0-255 range to 0.0-1.0
                if r > 1.0 or g > 1.0 or b > 1.0:
                    r, g, b = r / 255.0, g / 255.0, b / 255.0
                if a > 1.0:
                    a = a / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, a)
        except (ValueError, TypeError):
            return default

    return default


def check_if_installed(framework_name):
    """Check if a PyObjC framework is installed and provide installation guidance."""
    try:
        import importlib.util

        spec = importlib.util.find_spec(framework_name)
        if spec is None:
            print(f"[!] {framework_name} is not installed.")
            print(f"   To use {framework_name} features, install it with:")
            print(f"   pip install pyobjc-framework-{framework_name}")
            return False
        return True
    except (ImportError, ValueError):
        return False
