#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
StackBar Controls - Standalone control creation functions.

This module provides standalone functions for creating UI controls that can be used
in StackMenuItem layouts without needing to reference the StackMenuItem instance.
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
)
import httpx
from .sfsymbol import SFSymbol
from .utils import parse_color

# Import SpriteKit for line chart
try:
    import SpriteKit

    SPRITEKIT_AVAILABLE = True
except ImportError:
    SPRITEKIT_AVAILABLE = False

# Import AVKit for video playback
try:
    import AVKit
    import AVFoundation

    AVKIT_AVAILABLE = True
except ImportError:
    AVKIT_AVAILABLE = False

# Import MapKit for maps
try:
    import MapKit

    MAPKIT_AVAILABLE = True
except ImportError:
    MAPKIT_AVAILABLE = False

# Import WebKit for web views
try:
    import WebKit

    WEBKIT_AVAILABLE = True
except ImportError:
    WEBKIT_AVAILABLE = False

# Global registry to keep delegate references alive
_delegate_registry = {}
import objc
import datetime


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
            if char == "Z":
                if NSApp.sendAction_to_from_(b"redo:", None, self):
                    return True

    return False


class Editing(NSTextField):
    """NSTextField with cut, copy, paste, undo and selectAll

    Supports both Command (⌘) and Control (^) key combinations for cross-platform compatibility:
    - ⌘C / ^C: Copy
    - ⌘V / ^V: Paste
    - ⌘X / ^X: Cut
    - ⌘Z / ^Z: Undo
    - ⌘A / ^A: Select All
    """

    def performKeyEquivalent_(self, event):
        return _perform_key_equivalent(self, event)


class SecureEditing(NSSecureTextField):
    """NSSecureTextField with cut, copy, paste, undo and selectAll

    Supports both Command (⌘) and Control (^) key combinations for cross-platform compatibility.
    Note: Copy is disabled for security reasons in secure text fields.
    """

    def performKeyEquivalent_(self, event):
        return _perform_key_equivalent(self, event)


class SearchFieldEditing(NSSearchField):
    """NSSearchField with cut, copy, paste, undo and selectAll

    Supports both Command (⌘) and Control (^) key combinations for cross-platform compatibility:
    - ⌘C / ^C: Copy
    - ⌘V / ^V: Paste
    - ⌘X / ^X: Cut
    - ⌘Z / ^Z: Undo
    - ⌘A / ^A: Select All
    """

    def performKeyEquivalent_(self, event):
        print(
            f"DEBUG SearchField performKeyEquivalent: {event.charactersIgnoringModifiers()}, modifiers: {event.modifierFlags()}"
        )
        # Try our custom key handling first
        if _perform_key_equivalent(self, event):
            print("DEBUG: _perform_key_equivalent returned True")
            return True
        # Fall back to super implementation
        result = objc.super(SearchFieldEditing, self).performKeyEquivalent_(event)
        print(f"DEBUG: super performKeyEquivalent returned {result}")
        return result

    def keyDown_(self, event):
        """Handle key down events directly for search field"""
        print(
            f"DEBUG SearchField keyDown: {event.charactersIgnoringModifiers()}, modifiers: {event.modifierFlags()}"
        )

        # Check for command key combinations
        modifiers = event.modifierFlags() & AppKit.NSDeviceIndependentModifierFlagsMask
        char = event.charactersIgnoringModifiers()

        if modifiers == AppKit.NSCommandKeyMask:
            print(f"DEBUG: Command key pressed with '{char}'")
            if char == "v":
                print("DEBUG: Command-V detected, calling paste")
                self.paste_(self)
                return
            elif char == "c":
                self.copy_(self)
                return
            elif char == "x":
                self.cut_(self)
                return
            elif char == "a":
                self.selectAll_(self)
                return

        # Try our custom key handling first
        if _perform_key_equivalent(self, event):
            return
        # Fall back to super implementation
        objc.super(SearchFieldEditing, self).keyDown_(event)

    def becomeFirstResponder(self):
        """Override to ensure edit menu is available"""
        result = objc.super(SearchFieldEditing, self).becomeFirstResponder()
        if result:
            # Enable edit menu when search field becomes first responder
            NSApp.updateWindows()
        return result

    def respondsToSelector_(self, selector):
        """Override to indicate we handle edit actions"""
        if selector in [
            b"copy:",
            b"paste:",
            b"cut:",
            b"selectAll:",
            b"undo:",
            b"redo:",
        ]:
            return True
        return objc.super(SearchFieldEditing, self).respondsToSelector_(selector)

    def validateMenuItem_(self, menuItem):
        """Validate edit menu items"""
        selector = menuItem.action()

        if selector == b"copy:":
            return self.selectedRange().length > 0
        elif selector == b"paste:":
            from AppKit import NSPasteboard

            pasteboard = NSPasteboard.generalPasteboard()
            return pasteboard.stringForType_(AppKit.NSPasteboardTypeString) is not None
        elif selector == b"cut:":
            return self.isEditable() and self.selectedRange().length > 0
        elif selector == b"selectAll:":
            return True
        elif selector in [b"undo:", b"redo:"]:
            return True

        return objc.super(SearchFieldEditing, self).validateMenuItem_(menuItem)

    def copy_(self, sender):
        """Handle copy action"""
        editor = self.currentEditor()
        if editor:
            editor.copy_(sender)
        else:
            objc.super(SearchFieldEditing, self).copy_(sender)

    def paste_(self, sender):
        """Handle paste action"""
        print(f"DEBUG: paste_ called, sender={sender}")
        editor = self.currentEditor()
        print(f"DEBUG: currentEditor={editor}")
        if editor:
            editor.paste_(sender)
        else:
            # If no editor, get clipboard and insert
            from AppKit import NSPasteboard

            pasteboard = NSPasteboard.generalPasteboard()
            text = pasteboard.stringForType_(AppKit.NSPasteboardTypeString)
            print(f"DEBUG: clipboard text={text}")
            if text:
                self.setStringValue_(text)

    def cut_(self, sender):
        """Handle cut action"""
        editor = self.currentEditor()
        if editor:
            editor.cut_(sender)
        else:
            objc.super(SearchFieldEditing, self).cut_(sender)

    def selectAll_(self, sender):
        """Handle select all action"""
        editor = self.currentEditor()
        if editor:
            editor.selectAll_(sender)
        else:
            objc.super(SearchFieldEditing, self).selectAll_(sender)


class LinkLabel(NSTextField):
    """Uneditable text field that displays a clickable link"""

    def initWithText_URL_(self, text: str, url: str):
        self = objc.super(LinkLabel, self).init()

        if not self:
            return

        attr_str = self.attributedStringWithLinkToURL_text_(url, text)
        self.setAttributedStringValue_(attr_str)
        self.url = NSURL.URLWithString_(url)
        self.setBordered_(False)
        self.setSelectable_(False)
        self.setEditable_(False)
        self.setBezeled_(False)
        self.setDrawsBackground_(False)

        return self

    def resetCursorRects(self):
        self.addCursorRect_cursor_(self.bounds(), AppKit.NSCursor.pointingHandCursor())

    def mouseDown_(self, event):
        AppKit.NSWorkspace.sharedWorkspace().openURL_(self.url)

    def mouseEntered_(self, event):
        AppKit.NSCursor.pointingHandCursor().push()

    def mouseExited_(self, event):
        AppKit.NSCursor.pop()

    def attributedStringWithLinkToURL_text_(self, url: str, text: str):
        linkAttributes = {
            AppKit.NSLinkAttributeName: NSURL.URLWithString_(url),
            AppKit.NSUnderlineStyleAttributeName: AppKit.NSUnderlineStyleSingle,
            AppKit.NSForegroundColorAttributeName: AppKit.NSColor.linkColor(),
            # AppKit.NSCursorAttributeName: AppKit.NSCursor.pointingHandCursor(),
        }
        return AppKit.NSAttributedString.alloc().initWithString_attributes_(
            text, linkAttributes
        )


class ComboBoxDelegate(NSObject):
    """Helper class to handle combo box events"""

    def initWithTarget_Action_(self, target: NSObject, action):
        self = objc.super(ComboBoxDelegate, self).init()
        if not self:
            return

        self.target = target
        self.action_change = action
        return self

    @objc.objc_method
    def comboBoxSelectionDidChange_(self, notification):
        if self.action_change:
            if type(self.action_change) == str:
                self.target.performSelector_withObject_(
                    self.action_change, notification.object()
                )
            else:
                self.action_change(notification.object())


class ControlDelegate(NSObject):
    """Universal delegate for handling control events"""

    def initWithCallback_(self, callback):
        self = objc.super(ControlDelegate, self).init()
        if not self:
            return None

        self.callback = callback
        return self

    def handleAction_(self, sender):
        """Universal action handler"""
        print(f"🔥 Action received from {type(sender).__name__}")
        if self.callback:
            try:
                if callable(self.callback):
                    self.callback(sender)
                    print(f"✅ Callback executed successfully")
                else:
                    print(f"❌ Callback is not callable: {type(self.callback)}")
            except Exception as e:
                print(f"❌ Error in callback: {e}")
        else:
            print(f"❌ No callback set")

    # Use the same universal handler for all actions
    controlAction_ = handleAction_
    searchFieldAction_ = handleAction_
    sliderAction_ = handleAction_
    checkboxAction_ = handleAction_
    datePickerAction_ = handleAction_
    timePickerAction_ = handleAction_
    radioButtonAction_ = handleAction_


class ComboBox(NSComboBox):
    """NSComboBox that stores a reference to its delegate

    Note:
        This is required to maintain a reference to the delegate, otherwise it will
        not be retained after the ComboBox is created.
    """

    def setDelegate_(self, delegate: NSObject | None):
        self.delegate = delegate
        if delegate is not None:
            objc.super(ComboBox, self).setDelegate_(delegate)


### helpers ###


class WrappingLabel(NSTextField):
    """NSTextField that properly handles text wrapping in menus"""

    def initWithText_fontSize_bold_color_maxLines_width_(
        self, text, font_size, bold, color, max_lines, width
    ):
        self = objc.super(WrappingLabel, self).init()
        if not self:
            return None

        self.max_lines = max_lines
        self.label_width = width
        self.setStringValue_(str(text))
        self.setEditable_(False)
        self.setBordered_(False)
        self.setDrawsBackground_(False)
        self.setBackgroundColor_(NSColor.clearColor())
        self.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Set font
        if bold:
            font = NSFont.boldSystemFontOfSize_(font_size)
        else:
            font = NSFont.systemFontOfSize_(font_size)
        self.setFont_(font)

        # Set color
        if color:
            if isinstance(color, str):
                if color == "gray":
                    color = NSColor.secondaryLabelColor()
                elif color in ["white", "black"]:
                    color = NSColor.labelColor()
                else:
                    color = NSColor.labelColor()
            self.setTextColor_(color)

        # Configure wrapping
        self.setLineBreakMode_(AppKit.NSLineBreakByWordWrapping)
        self.cell().setWraps_(True)
        self.cell().setScrollable_(False)
        self.cell().setUsesSingleLineMode_(False)

        if max_lines > 0:
            self.setMaximumNumberOfLines_(max_lines)
            self.setLineBreakMode_(AppKit.NSLineBreakByTruncatingTail)

        # Set preferred max layout width to enable wrapping
        if width:
            self.setPreferredMaxLayoutWidth_(width)
            # Add width constraint
            self.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
        else:
            self.setPreferredMaxLayoutWidth_(250)

        return self

    def layout(self):
        """Recalculate cell size on each layout pass"""
        objc.super(WrappingLabel, self).layout()
        # Force cell to recalculate its size
        self.cell().setWraps_(True)
        self.invalidateIntrinsicContentSize()


def label(
    text, font_size=13, bold=False, color=None, wraps=False, max_lines=0, width=None
):
    """Create a text label.

    Args:
        text: The text to display
        font_size: Font size in points
        bold: Whether to use bold font
        color: Text color (NSColor or color name string)
        wraps: Whether text should wrap when exceeding menu width (default: False)
        max_lines: Maximum number of lines (0 = unlimited, default: 0)
        width: Width constraint in points (required when wraps=True for proper layout)

    Returns:
        NSTextField configured as a label
    """
    if wraps:
        # Use custom wrapping label class
        label = WrappingLabel.alloc().initWithText_fontSize_bold_color_maxLines_width_(
            text, font_size, bold, color, max_lines, width
        )
        return label

    # Standard non-wrapping label
    label = NSTextField.labelWithString_(str(text))
    label.setEditable_(False)
    label.setBordered_(False)
    label.setBackgroundColor_(NSColor.clearColor())
    label.setTranslatesAutoresizingMaskIntoConstraints_(False)

    if bold:
        font = NSFont.boldSystemFontOfSize_(font_size)
    else:
        font = NSFont.systemFontOfSize_(font_size)
    label.setFont_(font)

    if color:
        if isinstance(color, str):
            if color == "gray":
                color = NSColor.secondaryLabelColor()
            elif color == "white":
                color = NSColor.labelColor()
            elif color == "black":
                color = NSColor.labelColor()
            else:
                color = NSColor.labelColor()
        label.setTextColor_(color)

    # Default truncation behavior
    label.setLineBreakMode_(AppKit.NSLineBreakByTruncatingTail)

    return label


def link(text: str, url: str) -> NSTextField:
    """Create a clickable link label"""
    link = LinkLabel.alloc().initWithText_URL_(text, url)
    link.setTranslatesAutoresizingMaskIntoConstraints_(False)
    return link


def image(image_path, width=None, height=None, scaling=None, border_radius=None):
    """Create an image view from a network URL, SFSymbol, or NSImage.

    Args:
        image_path: SFSymbol instance, NSImage object, or URL string (http:// or https://)
        width: Optional width constraint
        height: Optional height constraint
        scaling: Optional NSImageScaling constant
        border_radius: Optional corner radius in points (e.g., 8.0 for rounded corners)

    Returns:
        NSImageView with the loaded image
    """
    try:
        image = None

        # Handle NSImage objects directly
        if isinstance(image_path, AppKit.NSImage):
            image = image_path
            if image:
                image.setScalesWhenResized_(True)
                original_size = image.size()

                # Calculate dimensions maintaining aspect ratio
                if width and height:
                    image.setSize_(NSMakeSize(width, height))
                elif width and not height:
                    aspect_ratio = (
                        original_size.height / original_size.width
                        if original_size.width > 0
                        else 1
                    )
                    height = width * aspect_ratio
                    image.setSize_(NSMakeSize(width, height))
                elif height and not width:
                    aspect_ratio = (
                        original_size.width / original_size.height
                        if original_size.height > 0
                        else 1
                    )
                    width = height * aspect_ratio
                    image.setSize_(NSMakeSize(width, height))

        # Handle SFSymbol instances
        elif isinstance(image_path, SFSymbol):
            image = image_path()  # Call SFSymbol to get NSImage
            if image:
                image.setScalesWhenResized_(True)
                original_size = image.size()

                # Calculate dimensions maintaining aspect ratio
                if width and height:
                    image.setSize_(NSMakeSize(width, height))
                elif width and not height:
                    aspect_ratio = original_size.height / original_size.width
                    height = width * aspect_ratio
                    image.setSize_(NSMakeSize(width, height))
                elif height and not width:
                    aspect_ratio = original_size.width / original_size.height
                    width = height * aspect_ratio
                    image.setSize_(NSMakeSize(width, height))

        # Handle network URLs
        elif isinstance(image_path, str) and (
            image_path.startswith("http://") or image_path.startswith("https://")
        ):
            # Fetch image data with httpx
            with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                response = client.get(image_path, headers={"User-Agent": "YourApp/1.0"})
                response.raise_for_status()
                image_data = response.content

            # Convert to NSData and create NSImage
            ns_data = NSData.dataWithBytes_length_(image_data, len(image_data))
            image = AppKit.NSImage.alloc().initWithData_(ns_data)

            if image and image.isValid():
                image.setScalesWhenResized_(True)
                original_size = image.size()

                # Calculate dimensions maintaining aspect ratio
                if width and height:
                    image.setSize_(NSMakeSize(width, height))
                elif width and not height:
                    # Scale height proportionally
                    aspect_ratio = original_size.height / original_size.width
                    height = width * aspect_ratio
                    image.setSize_(NSMakeSize(width, height))
                elif height and not width:
                    # Scale width proportionally
                    aspect_ratio = original_size.width / original_size.height
                    width = height * aspect_ratio
                    image.setSize_(NSMakeSize(width, height))
            else:
                raise ValueError("Failed to create valid image from URL")
        else:
            raise ValueError(f"Unsupported image type: {type(image_path)}")

        if not image:
            raise ValueError("Failed to create image")

        # Create image view
        image_view = NSImageView.imageViewWithImage_(image)
        image_view.setTranslatesAutoresizingMaskIntoConstraints_(False)

        if scaling is not None:
            image_view.setImageScaling_(scaling)
        else:
            image_view.setImageScaling_(AppKit.NSImageScaleProportionallyUpOrDown)

        if width:
            image_view.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
        if height:
            image_view.heightAnchor().constraintEqualToConstant_(height).setActive_(
                True
            )

        # Apply border radius if specified
        if border_radius is not None:
            image_view.setWantsLayer_(True)
            image_view.layer().setCornerRadius_(border_radius)
            image_view.layer().setMasksToBounds_(True)

        return image_view

    except Exception as e:
        print(f"Error loading image from {image_path}: {e}")
        return NSView.alloc().init()  # Return empty view on error


def button(
    title=None,
    target=None,
    action=None,
    style="default",
    image=None,
    image_position="left",
):
    """Create a button.

    Args:
        title: Button title text (optional if image is provided)
        target: Target object for the action
        action: Action selector string
        style: Button style - "default" (blue primary), "rounded" (standard),
               "inline", "textured", "rounded-rect", "recessed", "disclosure"
        image: Optional image - can be SFSymbol, NSImage, or path string
        image_position: Position of image relative to title - "left", "right", "above", "below", "only"

    Returns:
        NSButton configured with title and/or image and action
    """
    from .sfsymbol import SFSymbol

    # Create button with title (empty string if no title)
    button_title = str(title) if title is not None else ""
    button = NSButton.buttonWithTitle_target_action_(button_title, target, action)
    button.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Handle image if provided
    if image is not None:
        ns_image = None

        # Convert image parameter to NSImage
        if isinstance(image, SFSymbol):
            ns_image = image._nsimage
        elif isinstance(image, AppKit.NSImage):
            ns_image = image
        elif isinstance(image, str):
            # Try as file path or SFSymbol name
            if os.path.exists(image):
                ns_image = AppKit.NSImage.alloc().initWithContentsOfFile_(image)
            else:
                # Try as SF Symbol name
                try:
                    sf_symbol = SFSymbol(image)
                    ns_image = sf_symbol.nsimage()
                except:
                    pass

        if ns_image:
            button.setImage_(ns_image)

            # Set image position
            if image_position == "left":
                button.setImagePosition_(AppKit.NSImageLeft)
            elif image_position == "right":
                button.setImagePosition_(AppKit.NSImageRight)
            elif image_position == "above":
                button.setImagePosition_(AppKit.NSImageAbove)
            elif image_position == "below":
                button.setImagePosition_(AppKit.NSImageBelow)
            elif image_position == "only":
                button.setImagePosition_(AppKit.NSImageOnly)
            else:
                button.setImagePosition_(AppKit.NSImageLeft)

    # Apply button style
    if style == "default" or style == "primary":
        # Blue default action button (responds to Return key)
        button.setBezelStyle_(AppKit.NSBezelStyleRounded)
        button.setKeyEquivalent_("\r")  # Return key
    elif style == "rounded":
        button.setBezelStyle_(AppKit.NSBezelStyleRounded)
    elif style == "inline":
        button.setBezelStyle_(AppKit.NSBezelStyleInline)
    elif style == "textured":
        button.setBezelStyle_(AppKit.NSBezelStyleTexturedSquare)
    elif style == "rounded-rect":
        button.setBezelStyle_(AppKit.NSBezelStyleRoundRect)
    elif style == "recessed":
        button.setBezelStyle_(AppKit.NSBezelStyleRecessed)
    elif style == "disclosure":
        button.setBezelStyle_(AppKit.NSBezelStyleDisclosure)
    else:
        # Default to rounded style
        button.setBezelStyle_(AppKit.NSBezelStyleRounded)

    # Set hugging priority to prevent button from expanding
    button.setContentHuggingPriority_forOrientation_(
        AppKit.NSLayoutPriorityDefaultHigh,
        AppKit.NSLayoutConstraintOrientationHorizontal,
    )
    button.setContentCompressionResistancePriority_forOrientation_(
        AppKit.NSLayoutPriorityDefaultHigh,
        AppKit.NSLayoutConstraintOrientationHorizontal,
    )

    return button


def spacer(priority=250):
    """Create a spacer view that expands to fill available space.

    Args:
        priority: Hugging priority (lower = more expansion)

    Returns:
        NSView configured as a spacer
    """
    spacer = NSView.alloc().init()
    spacer.setTranslatesAutoresizingMaskIntoConstraints_(False)
    spacer.setContentHuggingPriority_forOrientation_(
        priority, AppKit.NSLayoutConstraintOrientationHorizontal
    )
    spacer.setContentHuggingPriority_forOrientation_(
        priority, AppKit.NSLayoutConstraintOrientationVertical
    )
    return spacer


def separator(vertical=False):
    """Create a separator line.

    Args:
        vertical: If True, creates a vertical separator; if False (default), creates horizontal

    Returns:
        NSBox configured as a separator line
    """
    from AppKit import NSBox

    separator = NSBox.alloc().init()
    separator.setBoxType_(AppKit.NSBoxSeparator)
    separator.setTranslatesAutoresizingMaskIntoConstraints_(False)

    if vertical:
        # Vertical separator
        separator.widthAnchor().constraintEqualToConstant_(1).setActive_(True)
        # Allow height to be determined by container
    else:
        # Horizontal separator (default)
        separator.heightAnchor().constraintEqualToConstant_(1).setActive_(True)
        # Allow width to be determined by container

    return separator


def progress_bar(
    value=0.0, indeterminate=False, dimensions=(200, 20), show_text=True, color=None
):
    """Create a horizontal progress bar.

    Args:
        value: Current progress value (0.0 to 1.0 for determinate, ignored for indeterminate)
        indeterminate: Whether to show indeterminate (spinning) progress. Default is False
        dimensions: A sequence of numbers whose length is two, specifying the dimensions of the progress bar
        show_text: Whether to show percentage text on the progress bar. Default is True
        color: Color of the progress bar (hex string or RGB tuple). Default is system accent color

    Returns:
        NSView containing a configured NSProgressIndicator
    """
    width, height = dimensions

    # Create the container view
    if show_text and not indeterminate:
        width = width - 35
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height + 10))
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Create progress indicator
    progress_height = min(height, 16)  # Progress bars work best at standard height
    progress_y = (height + 10 - progress_height) // 2

    progress = NSProgressIndicator.alloc().initWithFrame_(
        NSMakeRect(5, progress_y, width - 10, progress_height)
    )

    # Configure progress indicator
    progress.setStyle_(0)  # NSProgressIndicatorBarStyle
    progress.setIndeterminate_(indeterminate)

    if indeterminate:
        progress.startAnimation_(None)
    else:
        progress.setMinValue_(0.0)
        progress.setMaxValue_(1.0)
        progress.setDoubleValue_(max(0.0, min(1.0, value)))

    # Set custom color if provided
    if color:
        try:
            ns_color = parse_color(color)
            if ns_color:
                try:
                    progress.setControlTint_(1)  # Use color tint if possible
                except:
                    pass
        except:
            pass

    container.addSubview_(progress)

    # Add percentage text if requested
    if show_text and not indeterminate:
        text_height = 12
        text_y = max(0, (height + 10 - text_height) // 2)

        text_field = NSTextField.alloc().initWithFrame_(
            NSMakeRect(width, text_y, 35, text_height)
        )
        text_field.setEditable_(False)
        text_field.setSelectable_(False)
        text_field.setBordered_(False)
        text_field.setDrawsBackground_(False)
        text_field.setAlignment_(2)  # NSTextAlignmentRight
        text_field.setFont_(NSFont.systemFontOfSize_(10))
        text_field.setTextColor_(NSColor.secondaryLabelColor())

        percentage = int(max(0.0, min(1.0, value)) * 100)
        text_field.setStringValue_(f"{percentage}%")
        container.addSubview_(text_field)

    return container


def circular_progress(
    value=0.0, indeterminate=False, dimensions=(40, 40), color=None, line_width=3.0
):
    """Create a circular progress indicator.

    Args:
        value: Current progress value (0.0 to 1.0 for determinate, ignored for indeterminate)
        indeterminate: Whether to show indeterminate (spinning) progress. Default is False
        dimensions: A sequence of numbers whose length is two, specifying the dimensions of the container
        color: Color of the progress indicator (hex string or RGB tuple). Default is system accent color
        line_width: Width of the progress circle line. Default is 3.0

    Returns:
        NSView containing a configured circular progress indicator
    """
    width, height = dimensions

    # Create the container view
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)

    if indeterminate:
        # Use NSProgressIndicator for indeterminate (spinning) mode
        size = min(width - 4, height - 4)
        x = (width - size) // 2
        y = (height - size) // 2

        progress = NSProgressIndicator.alloc().initWithFrame_(
            NSMakeRect(x, y, size, size)
        )
        progress.setStyle_(1)  # 1 = NSProgressIndicatorSpinningStyle
        progress.setDisplayedWhenStopped_(True)
        progress.setUsesThreadedAnimation_(True)
        progress.setIndeterminate_(True)
        progress.startAnimation_(None)

        container.addSubview_(progress)
    else:
        # Use custom view for determinate progress
        ns_color = parse_color(color) if color else None

        custom_view = _create_circular_progress_view(
            NSMakeRect(2, 2, width - 4, height - 4),
            max(0.0, min(1.0, value)),
            ns_color,
            line_width,
        )
        container.addSubview_(custom_view)

    return container


def _create_circular_progress_view(frame, value, color, line_width):
    """Create a custom circular progress view."""

    class CircularProgressView(NSView):
        def initWithFrame_value_color_lineWidth_(self, frame, value, color, line_width):
            self = objc.super(CircularProgressView, self).initWithFrame_(frame)
            if self:
                self._value = float(value) if value is not None else 0.0
                self._color = color or NSColor.colorWithSRGBRed_green_blue_alpha_(
                    0x7F / 255.0, 0x84 / 255.0, 0x8A / 255.0, 1.0
                )
                self._line_width = max(2.0, float(line_width) if line_width else 8.0)
                self.setWantsLayer_(True)
            return self

        def drawRect_(self, _rect):
            bounds = self.bounds()
            w, h = bounds.size.width, bounds.size.height
            cx, cy = w * 0.5, h * 0.5
            radius = max(0.0, min(w, h) * 0.5 - self._line_width * 0.5)
            if radius <= 0:
                return

            # Track (background ring)
            track = NSBezierPath.bezierPath()
            track.setLineWidth_(self._line_width)
            track.appendBezierPathWithOvalInRect_(
                NSMakeRect(cx - radius, cy - radius, radius * 2, radius * 2)
            )
            NSColor.colorWithCalibratedWhite_alpha_(0.17, 1.0).set()
            track.stroke()

            # Progress arc
            v = max(0.0, min(1.0, float(self._value)))
            if v > 0.0:
                start_deg = 90.0
                end_deg = start_deg - (v * 360.0)
                arc = NSBezierPath.bezierPath()
                arc.setLineWidth_(self._line_width)
                arc.setLineCapStyle_(NSRoundLineCapStyle)
                arc.appendBezierPathWithArcWithCenter_radius_startAngle_endAngle_clockwise_(
                    NSMakePoint(cx, cy), radius, start_deg, end_deg, True
                )
                (self._color or NSColor.systemBlueColor()).set()
                arc.stroke()

    return CircularProgressView.alloc().initWithFrame_value_color_lineWidth_(
        frame, value, color, line_width
    )


def slider(value=50, min_value=0, max_value=100, width=180, height=15, callback=None):
    """Create a slider control.

    Args:
        value: Initial value of the slider
        min_value: Minimum value of the slider
        max_value: Maximum value of the slider
        width: Width of the slider in points
        height: Height of the slider in points
        callback: Function to call when slider value changes

    Returns:
        NSSlider configured with the specified parameters
    """
    from AppKit import NSSlider, NSSize

    slider = NSSlider.alloc().init()
    slider.setMinValue_(min_value)
    slider.setMaxValue_(max_value)
    slider.setDoubleValue_(value)
    slider.setFrameSize_(NSSize(width, height))
    slider.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Set up constraints for size
    slider.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    slider.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    # Set up callback using NSApp and StackAppDelegate
    if callback:
        from .delegate import StackAppDelegate

        slider.setTarget_(NSApp)
        slider.setAction_("sliderCallback:")
        # Register callback with delegate
        StackAppDelegate.register_callback(slider, None, callback)

    return slider


def checkbox(title="", checked=False, callback=None):
    """Create a checkbox control.

    Args:
        title: Text label for the checkbox
        checked: Initial checked state
        callback: Function to call when checkbox is toggled

    Returns:
        NSButton configured as a checkbox
    """
    from AppKit import NSButton

    checkbox = NSButton.buttonWithTitle_target_action_(str(title), None, None)
    checkbox.setButtonType_(AppKit.NSButtonTypeSwitch)
    checkbox.setState_(
        AppKit.NSControlStateValueOn if checked else AppKit.NSControlStateValueOff
    )
    checkbox.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Set up callback using NSApp and StackAppDelegate
    if callback:
        from .delegate import StackAppDelegate

        checkbox.setTarget_(NSApp)
        checkbox.setAction_("checkboxCallback:")
        # Register callback with delegate
        StackAppDelegate.register_callback(checkbox, None, callback)

    return checkbox


def combobox(
    items=None, selected_index=-1, width=200, height=22, callback=None, editable=False
):
    """Create a combobox/dropdown control.

    Args:
        items: List of items to display in the dropdown
        selected_index: Index of initially selected item (-1 for none)
        width: Width of the combobox in points
        height: Height of the combobox in points
        callback: Function to call when selection changes
        editable: Whether the combobox is editable

    Returns:
        NSComboBox configured with the specified parameters
    """

    combobox = ComboBox.alloc().init()
    combobox.setFrameSize_(NSSize(width, height))
    combobox.setTranslatesAutoresizingMaskIntoConstraints_(False)
    combobox.setEditable_(editable)

    # Add items if provided
    if items:
        for item in items:
            combobox.addItemWithObjectValue_(str(item))

    # Set selected index if valid
    if 0 <= selected_index < len(items or []):
        combobox.selectItemAtIndex_(selected_index)

    # Set up constraints for size
    combobox.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    combobox.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    # Set up callback using NSApp and StackAppDelegate
    if callback:
        from .delegate import StackAppDelegate

        combobox.setTarget_(NSApp)
        combobox.setAction_("comboboxCallback:")
        # Register callback with delegate
        StackAppDelegate.register_callback(combobox, None, callback)

    return combobox


def text_field(
    size: tuple[float, float] = (200, 25),
    placeholder: str | None = None,
    target: NSObject | None = None,
    action=None,
    border_radius: float = 25.0,
    **kwargs,
) -> NSTextField:
    """Create a text field.

    Args:
        size: width, height of the text field
        placeholder: placeholder text
        target: target to send action to
        action: action to send when the date is changed
        border_radius: border radius
        **kwargs: additional keyword/value attributes to configure

    Returns NSTextField
    """
    text_field = Editing.alloc().initWithFrame_(NSMakeRect(0, 0, *size))
    text_field.setBezeled_(True)
    text_field.setBordered_(True)
    text_field.setBezelStyle_(AppKit.NSTextFieldSquareBezel)
    text_field.setTranslatesAutoresizingMaskIntoConstraints_(False)
    text_field.setWantsLayer_(True)
    # Don't call becomeFirstResponder() automatically - it can interfere with menu interaction
    width_constraint = text_field.widthAnchor().constraintEqualToConstant_(size[0])
    width_constraint.setActive_(True)
    height_constraint = text_field.heightAnchor().constraintEqualToConstant_(size[1])
    height_constraint.setActive_(True)
    if placeholder:
        text_field.setPlaceholderString_(placeholder)
    if target:
        text_field.setTarget_(target)
    if action:
        text_field.setAction_(action)
    if border_radius:
        text_field.layer().setCornerRadius_(border_radius)
    if kwargs:
        for key, value in kwargs.items():
            method = f"set{key[0].upper()}{key[1:]}_"
            if hasattr(text_field, method):
                getattr(text_field, method)(value)

    return text_field


def secure_text_input(text="", placeholder="", width=200, height=22, callback=None):
    """Create a secure text input field (for passwords).

    Args:
        text: Initial text content
        placeholder: Placeholder text to show when empty
        width: Width of the text field in points
        height: Height of the text field in points
        callback: Function to call when text changes

    Returns:
        NSSecureTextField configured as a secure text input
    """
    # Create a secure text field with proper key handling
    text_field = SecureEditing.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    text_field.setStringValue_(str(text))
    text_field.setTranslatesAutoresizingMaskIntoConstraints_(False)
    text_field.setEditable_(True)
    text_field.setSelectable_(True)
    text_field.setBordered_(True)
    text_field.setBezelStyle_(AppKit.NSTextFieldSquareBezel)

    # Set placeholder if provided
    if placeholder:
        text_field.setPlaceholderString_(str(placeholder))

    # Set up constraints for size
    text_field.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    text_field.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    # Note: Callback handling would need to be implemented in the app delegate
    # For now, we'll skip storing the callback since NSSecureTextField doesn't allow custom attributes
    # In a full implementation, callbacks would be handled through the delegate system

    return text_field


class SearchFieldWithShortcuts(NSView):
    """Container view for search field that handles keyboard shortcuts."""

    def initWithSearchField_(self, search_field):
        self = objc.super(SearchFieldWithShortcuts, self).init()
        if not self:
            return None

        self.search_field = search_field
        self.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Add search field as subview
        self.addSubview_(search_field)

        # Set constraints to match search field size
        search_field.topAnchor().constraintEqualToAnchor_(self.topAnchor()).setActive_(
            True
        )
        search_field.bottomAnchor().constraintEqualToAnchor_(
            self.bottomAnchor()
        ).setActive_(True)
        search_field.leadingAnchor().constraintEqualToAnchor_(
            self.leadingAnchor()
        ).setActive_(True)
        search_field.trailingAnchor().constraintEqualToAnchor_(
            self.trailingAnchor()
        ).setActive_(True)

        return self

    def performKeyEquivalent_(self, event):
        """Intercept key equivalents and forward to search field."""
        modifiers = event.modifierFlags() & AppKit.NSDeviceIndependentModifierFlagsMask
        char = event.charactersIgnoringModifiers()

        if modifiers == AppKit.NSCommandKeyMask:
            if char == "v":
                self.search_field.paste_(self)
                return True
            elif char == "c":
                self.search_field.copy_(self)
                return True
            elif char == "x":
                self.search_field.cut_(self)
                return True
            elif char == "a":
                self.search_field.selectAll_(self)
                return True

        return objc.super(SearchFieldWithShortcuts, self).performKeyEquivalent_(event)


def search_field(
    size: tuple[float, float] = (200, 25),
    target: NSObject | None = None,
    action=None,
    placeholder: str = None,
    **kwargs,
):
    """Create a search field with copy/paste keyboard shortcut support.

    Args:
        size: width, height of the text field
        target: target to send action to
        action: action to send when the search field is used
        placeholder: placeholder text
        **kwargs: additional keyword/value attributes to configure

    Returns SearchFieldWithShortcuts container with NSSearchField inside

    Note: Returns a container view. To access the search field directly, use .search_field attribute.
    """
    # Use the custom SearchFieldEditing class for keyboard shortcut support
    search_field_control = SearchFieldEditing.alloc().initWithFrame_(
        NSMakeRect(0, 0, *size)
    )

    # Enable proper text editing behavior
    search_field_control.setEditable_(True)
    search_field_control.setSelectable_(True)
    search_field_control.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Set size constraints
    search_field_control.widthAnchor().constraintEqualToConstant_(size[0]).setActive_(
        True
    )
    search_field_control.heightAnchor().constraintEqualToConstant_(size[1]).setActive_(
        True
    )

    # Enable standard text editing features
    search_field_control.setImportsGraphics_(False)
    search_field_control.setAllowsEditingTextAttributes_(False)

    # Make sure the search field can become first responder
    search_field_control.setRefusesFirstResponder_(False)

    # Handle target/action
    if target:
        search_field_control.setTarget_(target)
    if action:
        search_field_control.setAction_(action)

    if placeholder:
        search_field_control.setPlaceholderString_(placeholder)

    if kwargs:
        for key, value in kwargs.items():
            method = f"set{key[0].upper()}{key[1:]}_"
            if hasattr(search_field_control, method):
                getattr(search_field_control, method)(value)

    # Wrap in container that handles keyboard shortcuts
    # container = SearchFieldWithShortcuts.alloc().initWithSearchField_(search_field_control)

    return search_field_control


def radio_button(
    title: str, target=None, action=None, callback=None, **kwargs
) -> NSButton:
    """Create a radio button

    Args:
            title: title text for the button
            target: target to send action to (takes precedence over callback)
            action: action to send when the selection is changed
            callback: Python function to call when radio button is selected
            **kwargs: additional keyword/value attributes to configure

    Returns: NSButton radio button
    """
    # Handle target/action vs callback
    if target and action:
        radio_button = NSButton.buttonWithTitle_target_action_(title, target, action)
    elif callback:
        from .delegate import StackAppDelegate

        radio_button = NSButton.buttonWithTitle_target_action_(
            title, NSApp, "radioButtonCallback:"
        )
        # Register callback with delegate
        StackAppDelegate.register_callback(radio_button, None, callback)
    else:
        radio_button = NSButton.buttonWithTitle_target_action_(title, None, None)

    radio_button.setButtonType_(AppKit.NSRadioButton)
    if kwargs:
        for key, value in kwargs.items():
            method = f"set{key[0].upper()}{key[1:]}_"
            if hasattr(radio_button, method):
                getattr(radio_button, method)(value)
    return radio_button


def radio_group(
    options: list[str] | list,
    selected: int = 0,
    orientation: str = "vertical",
    spacing: float = 8.0,
    callback=None,
    **kwargs,
) -> "StackView":
    """Create a group of mutually exclusive radio buttons

    Args:
        options: List of radio button labels (strings) or pre-configured NSButton radio buttons
        selected: Index of initially selected option (default: 0)
        orientation: "vertical" or "horizontal" layout (default: "vertical")
        spacing: Spacing between radio buttons in points (default: 8.0)
        callback: Python function called when selection changes.
                  Receives the NSButton that was selected.
        **kwargs: Additional keyword/value attributes (only applied when options are strings)

    Returns: StackView containing the radio button group
    """
    from .core import hstack, vstack
    from .delegate import StackAppDelegate

    # Create radio buttons
    radio_buttons = []
    for i, option in enumerate(options):
        # Check if option is already an NSButton or a string
        if isinstance(option, str):
            # Create new radio button from string
            rb = NSButton.buttonWithTitle_target_action_(option, None, None)
            rb.setButtonType_(AppKit.NSRadioButton)
            rb.setState_(AppKit.NSOnState if i == selected else AppKit.NSOffState)

            # Apply additional kwargs
            if kwargs:
                for key, value in kwargs.items():
                    method = f"set{key[0].upper()}{key[1:]}_"
                    if hasattr(rb, method):
                        getattr(rb, method)(value)
        else:
            # Use pre-configured radio button
            rb = option
            # Ensure it's set as radio button type
            rb.setButtonType_(AppKit.NSRadioButton)
            rb.setState_(AppKit.NSOnState if i == selected else AppKit.NSOffState)

        radio_buttons.append(rb)

    # Set up mutual exclusivity - when one is clicked, uncheck others
    def create_radio_callback(button_index, all_buttons):
        def radio_selected(sender):
            # Uncheck all other buttons
            for i, btn in enumerate(all_buttons):
                if i != button_index:
                    btn.setState_(AppKit.NSOffState)
                else:
                    btn.setState_(AppKit.NSOnState)

            # Call user callback if provided
            if callback:
                callback(sender)

        return radio_selected

    # Register callbacks for each button
    for i, rb in enumerate(radio_buttons):
        rb.setTarget_(NSApp)
        rb.setAction_("radioGroupCallback:")
        StackAppDelegate.register_callback(
            rb, None, create_radio_callback(i, radio_buttons)
        )

    # Create stack layout
    if orientation == "horizontal":
        container = hstack(radio_buttons, spacing=spacing)
    else:
        container = vstack(radio_buttons, spacing=spacing)

    return container


def date_picker(
    style: int = AppKit.NSDatePickerStyleClockAndCalendar,
    elements: int = AppKit.NSDatePickerElementFlagYearMonthDay,
    mode: int = AppKit.NSDatePickerModeSingle,
    date: datetime.date | datetime.datetime | None = None,
    target: NSObject | None = None,
    action=None,
    size: tuple[int, int] = (200, 50),
    callback=None,
    **kwargs,
) -> NSDatePicker:
    """Create a date picker

    Args:
        style: style of the date picker, an AppKit.NSDatePickerStyle
        elements: elements to display in the date picker, an AppKit.NSDatePickerElementFlag
        mode: mode of the date picker, an AppKit.NSDatePickerMode
        date: initial date of the date picker; if None, defaults to the current date
        target: target to send action to (takes precedence over callback)
        action: action to send when the date is changed
        size: size of the date picker
        callback: Python function to call when date changes
        **kwargs: additional keyword/value attributes to configure

    Returns: NSDatePicker
    """
    date = date or datetime.date.today()
    date_picker = NSDatePicker.alloc().initWithFrame_(NSMakeRect(0, 0, *size))
    date_picker.setDatePickerStyle_(style)
    date_picker.setDatePickerElements_(elements)
    date_picker.setDatePickerMode_(mode)
    date_picker.setDateValue_(date)
    date_picker.setTimeZone_(NSTimeZone.localTimeZone())
    date_picker.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Handle target/action vs callback
    if target and action:
        date_picker.setTarget_(target)
        date_picker.setAction_(action)
    elif callback:
        from .delegate import StackAppDelegate

        date_picker.setTarget_(NSApp)
        date_picker.setAction_("datePickerCallback:")
        # Register callback with delegate
        StackAppDelegate.register_callback(date_picker, None, callback)

    if kwargs:
        for key, value in kwargs.items():
            method = f"set{key[0].upper()}{key[1:]}_"
            if hasattr(date_picker, method):
                getattr(date_picker, method)(value)
    return date_picker


def time_picker(
    style: int = AppKit.NSDatePickerStyleTextFieldAndStepper,
    elements: int = AppKit.NSDatePickerElementFlagHourMinute,
    mode: int = AppKit.NSDatePickerModeSingle,
    time: datetime.datetime | datetime.time | None = None,
    target: NSObject | None = None,
    action=None,
    callback=None,
    **kwargs,
) -> NSDatePicker:
    """Create a time picker

    Args:
        style: style of the date picker, an AppKit.NSDatePickerStyle
        elements: elements to display in the date picker, an AppKit.NSDatePickerElementFlag
        mode: mode of the date picker, an AppKit.NSDatePickerMode
        time: initial time of the date picker; if None, defaults to the current time
        target: target to send action to (takes precedence over callback)
        action: action to send when the time is changed
        callback: Python function to call when time changes
        **kwargs: additional keyword/value attributes to configure

    Returns: NSDatePicker


    Note: This function is a wrapper around date_picker, with the date picker style set to
    display a time picker.
    """
    # if time is only a time, convert to datetime with today's date
    # as the date picker requires a datetime or date
    if isinstance(time, datetime.time):
        time = datetime.datetime.combine(datetime.date.today(), time)
    time = time or datetime.datetime.now()
    tp = date_picker(
        style=style,
        elements=elements,
        mode=mode,
        date=time,
        target=target,
        action=action,
        callback=callback,
    )
    if kwargs:
        for key, value in kwargs.items():
            method = f"set{key[0].upper()}{key[1:]}_"
            if hasattr(tp, method):
                getattr(tp, method)(value)
    return tp


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


def line_chart(
    points=None,
    dimensions=(60, 20),
    max_value=100.0,
    min_value=0.0,
    color=None,
    line_width=0.5,
    fill=True,
    show_axes=False,
    show_grid=False,
    x_labels=None,
    y_labels=None,
    axis_color=None,
    grid_color=None,
):
    """Create a line chart with smooth spline interpolation using SpriteKit.

    Args:
        points: List of data points (0.0 to max_value)
        dimensions: Tuple of (width, height) in points
        max_value: Maximum value for scaling (default: 100.0)
        min_value: Minimum value for scaling (default: 0.0)
        color: Line color (hex string or NSColor, default: label color)
        line_width: Width of the line stroke (default: 0.5)
        fill: Whether to fill under the line (default: True)
        show_axes: Whether to show X and Y axes (default: False)
        show_grid: Whether to show grid lines (default: False)
        x_labels: List of labels for X-axis tick marks (optional)
        y_labels: List of labels for Y-axis tick marks (optional)
        axis_color: Color for axes and labels (default: secondary label color)
        grid_color: Color for grid lines (default: separator color)

    Returns:
        NSView containing the line chart
    """
    if points is None:
        points = []

    width, height = dimensions

    # Create container view
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)
    container.setWantsLayer_(True)

    # Set size constraints
    container.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    container.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    if len(points) < 2:
        # Return empty view if not enough points
        return container

    # Parse colors
    chart_color = parse_color(color, default=NSColor.labelColor())
    parsed_axis_color = parse_color(axis_color, default=NSColor.secondaryLabelColor())
    parsed_grid_color = parse_color(grid_color, default=NSColor.separatorColor())

    # Create custom view with spline interpolation
    chart_view = _LineChartView.alloc().initWithFrame_points_maxValue_minValue_color_lineWidth_fill_showAxes_showGrid_xLabels_yLabels_axisColor_gridColor_(
        NSMakeRect(0, 0, width, height),
        points,
        max_value,
        min_value,
        chart_color,
        line_width,
        fill,
        show_axes,
        show_grid,
        x_labels if x_labels else [],
        y_labels if y_labels else [],
        parsed_axis_color,
        parsed_grid_color,
    )

    container.addSubview_(chart_view)

    return container


class _LineChartView(NSView):
    """Custom view for rendering line charts with spline interpolation."""

    def initWithFrame_points_maxValue_minValue_color_lineWidth_fill_showAxes_showGrid_xLabels_yLabels_axisColor_gridColor_(
        self,
        frame,
        points,
        max_value,
        min_value,
        color,
        line_width,
        fill,
        show_axes,
        show_grid,
        x_labels,
        y_labels,
        axis_color,
        grid_color,
    ):
        self = objc.super(_LineChartView, self).initWithFrame_(frame)
        if not self:
            return None

        self._points = list(points)
        self._max_value = float(max_value)
        self._min_value = float(min_value)
        self._color = color
        self._line_width = float(line_width)
        self._fill = fill
        self._show_axes = show_axes
        self._show_grid = show_grid
        self._x_labels = list(x_labels) if x_labels else []
        self._y_labels = list(y_labels) if y_labels else []
        self._axis_color = axis_color
        self._grid_color = grid_color
        self.setWantsLayer_(True)

        return self

    def py_convert_value_to_y(self, value, chart_height, margin_bottom):
        """Convert data value to y coordinate."""
        normalized = (value - self._min_value) / (self._max_value - self._min_value)
        return margin_bottom + max(
            0.5, min(chart_height - 0.5, normalized * chart_height)
        )

    def py_create_spline_path(self):
        """Create bezier path with spline interpolation using SpriteKit."""
        bounds = self.bounds()
        width = bounds.size.width
        height = bounds.size.height

        # Calculate chart area (same as in drawRect_)
        margin_left = 20.0 if self._show_axes and self._y_labels else 0.0
        margin_bottom = 10.0 if self._show_axes and self._x_labels else 0.0
        chart_width = width - margin_left
        chart_height = height - margin_bottom

        if len(self._points) < 2:
            return NSBezierPath.bezierPath()

        # Calculate step between points
        step_x = chart_width / (len(self._points) - 1)

        # Convert points to coordinates (offset by left margin)
        x_points = [margin_left + step_x * i for i in range(len(self._points))]
        y_points = [
            self.py_convert_value_to_y(p, chart_height, margin_bottom)
            for p in self._points
        ]

        if SPRITEKIT_AVAILABLE:
            try:
                # Use SpriteKit keyframe sequence for spline interpolation
                sequence = (
                    SpriteKit.SKKeyframeSequence.alloc().initWithKeyframeValues_times_(
                        y_points, [NSNumber.numberWithDouble_(x) for x in x_points]
                    )
                )
                sequence.setInterpolationMode_(SpriteKit.SKInterpolationModeSpline)

                # Sample the spline at regular intervals
                path = NSBezierPath.bezierPath()
                sample_step = 0.5
                min_x = x_points[0]  # Start x (with margin)
                max_x = x_points[-1]  # End x (with margin)

                # Start at first point
                first_y = sequence.sampleAtTime_(min_x)
                if isinstance(first_y, (int, float)):
                    path.moveToPoint_(NSMakePoint(min_x, first_y))
                else:
                    path.moveToPoint_(NSMakePoint(min_x, y_points[0]))

                # Sample along the curve
                x = min_x + sample_step
                while x <= max_x:
                    sampled_y = sequence.sampleAtTime_(x)
                    if isinstance(sampled_y, (int, float)):
                        y = sampled_y
                    else:
                        # Fallback to linear interpolation
                        # Find which segment we're in
                        idx = int((x - min_x) / step_x)
                        if idx >= len(y_points) - 1:
                            y = y_points[-1]
                        else:
                            t = (x - x_points[idx]) / step_x
                            y = y_points[idx] * (1 - t) + y_points[idx + 1] * t
                    path.lineToPoint_(NSMakePoint(x, y))
                    x += sample_step

                # End at last point
                last_y = sequence.sampleAtTime_(max_x)
                if isinstance(last_y, (int, float)):
                    path.lineToPoint_(NSMakePoint(max_x, last_y))
                else:
                    path.lineToPoint_(NSMakePoint(max_x, y_points[-1]))

                return path

            except Exception as e:
                print(f"SpriteKit spline interpolation failed: {e}")
                # Fall through to simple line rendering

        # Fallback: simple line chart without spline interpolation
        path = NSBezierPath.bezierPath()
        path.moveToPoint_(NSMakePoint(x_points[0], y_points[0]))
        for i in range(1, len(self._points)):
            path.lineToPoint_(NSMakePoint(x_points[i], y_points[i]))

        return path

    def drawRect_(self, dirty_rect):
        """Draw the line chart."""
        bounds = self.bounds()
        width = bounds.size.width
        height = bounds.size.height

        # Calculate chart area (reserve space for axes if needed)
        margin_left = 20.0 if self._show_axes and self._y_labels else 0.0
        margin_bottom = 10.0 if self._show_axes and self._x_labels else 0.0
        chart_width = width - margin_left
        chart_height = height - margin_bottom

        # Draw grid if enabled
        if self._show_grid:
            self._grid_color.setStroke()
            grid_path = NSBezierPath.bezierPath()
            grid_path.setLineWidth_(0.5)

            # Vertical grid lines (for x_labels)
            if self._x_labels:
                num_x_lines = len(self._x_labels)
                for i in range(num_x_lines):
                    x = margin_left + (
                        chart_width / (num_x_lines - 1) * i
                        if num_x_lines > 1
                        else chart_width / 2
                    )
                    grid_path.moveToPoint_(NSMakePoint(x, margin_bottom))
                    grid_path.lineToPoint_(NSMakePoint(x, height))

            # Horizontal grid lines (for y_labels)
            if self._y_labels:
                num_y_lines = len(self._y_labels)
                for i in range(num_y_lines):
                    y = margin_bottom + (
                        chart_height / (num_y_lines - 1) * i
                        if num_y_lines > 1
                        else chart_height / 2
                    )
                    grid_path.moveToPoint_(NSMakePoint(margin_left, y))
                    grid_path.lineToPoint_(NSMakePoint(width, y))

            grid_path.stroke()

        # Draw axes if enabled
        if self._show_axes:
            self._axis_color.setStroke()
            axis_path = NSBezierPath.bezierPath()
            axis_path.setLineWidth_(1.0)

            # Y-axis (left)
            axis_path.moveToPoint_(NSMakePoint(margin_left, margin_bottom))
            axis_path.lineToPoint_(NSMakePoint(margin_left, height))

            # X-axis (bottom)
            axis_path.moveToPoint_(NSMakePoint(margin_left, margin_bottom))
            axis_path.lineToPoint_(NSMakePoint(width, margin_bottom))

            axis_path.stroke()

            # Draw axis labels
            font = NSFont.systemFontOfSize_(8.0)
            attrs = {
                AppKit.NSFontAttributeName: font,
                AppKit.NSForegroundColorAttributeName: self._axis_color,
            }

            # X-axis labels
            if self._x_labels:
                num_x_labels = len(self._x_labels)
                for i, label in enumerate(self._x_labels):
                    x = margin_left + (
                        chart_width / (num_x_labels - 1) * i
                        if num_x_labels > 1
                        else chart_width / 2
                    )

                    # Create NSAttributedString
                    label_str = Foundation.NSString.stringWithString_(str(label))
                    attr_string = (
                        AppKit.NSAttributedString.alloc().initWithString_attributes_(
                            label_str, attrs
                        )
                    )
                    label_size = attr_string.size()

                    label_rect = NSMakeRect(
                        x - label_size.width / 2,
                        margin_bottom - label_size.height - 2,
                        label_size.width,
                        label_size.height,
                    )
                    attr_string.drawInRect_(label_rect)

            # Y-axis labels
            if self._y_labels:
                num_y_labels = len(self._y_labels)
                for i, label in enumerate(self._y_labels):
                    y = margin_bottom + (
                        chart_height / (num_y_labels - 1) * i
                        if num_y_labels > 1
                        else chart_height / 2
                    )

                    # Create NSAttributedString
                    label_str = Foundation.NSString.stringWithString_(str(label))
                    attr_string = (
                        AppKit.NSAttributedString.alloc().initWithString_attributes_(
                            label_str, attrs
                        )
                    )
                    label_size = attr_string.size()

                    label_rect = NSMakeRect(
                        margin_left - label_size.width - 4,
                        y - label_size.height / 2,
                        label_size.width,
                        label_size.height,
                    )
                    attr_string.drawInRect_(label_rect)

        # Get the spline path
        path = self.py_create_spline_path()

        if self._fill:
            # Create closed path for fill
            filled_path = path.copy()
            # Add lines to close the path at bottom (accounting for margins)
            filled_path.lineToPoint_(
                NSMakePoint(
                    width - (0 if not (self._show_axes and self._y_labels) else 0),
                    margin_bottom,
                )
            )
            filled_path.lineToPoint_(NSMakePoint(margin_left, margin_bottom))
            filled_path.closePath()

            # Fill with semi-transparent color
            fill_color = self._color.colorWithAlphaComponent_(0.3)
            fill_color.setFill()
            filled_path.fill()

        # Draw the stroke
        path.setLineWidth_(self._line_width)
        path.setLineJoinStyle_(AppKit.NSLineJoinStyleRound)
        path.setLineCapStyle_(NSRoundLineCapStyle)
        self._color.setStroke()
        path.stroke()


def bar_chart(
    values=None,
    dimensions=(60, 20),
    max_value=100.0,
    min_value=0.0,
    color=None,
    bar_spacing=1.0,
    corner_radius=1.0,
    show_axes=False,
    show_grid=False,
    x_labels=None,
    y_labels=None,
    axis_color=None,
    grid_color=None,
):
    """Create a bar chart using NSView drawing.

    Args:
        values: List of data values
        dimensions: Tuple of (width, height) in points
        max_value: Maximum value for scaling
        min_value: Minimum value for scaling
        color: Bar color (hex string or NSColor)
        bar_spacing: Space between bars in points
        corner_radius: Rounded corner radius
        show_axes: Whether to show X and Y axes (default: False)
        show_grid: Whether to show grid lines (default: False)
        x_labels: List of labels for X-axis tick marks (optional)
        y_labels: List of labels for Y-axis tick marks (optional)
        axis_color: Color for axes and labels (default: secondary label color)
        grid_color: Color for grid lines (default: separator color)

    Returns:
        NSView containing the bar chart
    """
    if values is None:
        values = []

    width, height = dimensions

    # Create container view
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)
    container.setWantsLayer_(True)

    container.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    container.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    if len(values) == 0:
        return container

    # Parse colors
    bar_color = parse_color(color, default=NSColor.systemGreenColor())
    parsed_axis_color = parse_color(axis_color, default=NSColor.secondaryLabelColor())
    parsed_grid_color = parse_color(grid_color, default=NSColor.separatorColor())

    # Create custom view
    chart_view = _BarChartView.alloc().initWithFrame_values_maxValue_minValue_color_spacing_cornerRadius_showAxes_showGrid_xLabels_yLabels_axisColor_gridColor_(
        NSMakeRect(0, 0, width, height),
        values,
        max_value,
        min_value,
        bar_color,
        bar_spacing,
        corner_radius,
        show_axes,
        show_grid,
        x_labels if x_labels else [],
        y_labels if y_labels else [],
        parsed_axis_color,
        parsed_grid_color,
    )

    container.addSubview_(chart_view)

    return container


class _BarChartView(NSView):
    """Custom view for rendering bar charts."""

    def initWithFrame_values_maxValue_minValue_color_spacing_cornerRadius_showAxes_showGrid_xLabels_yLabels_axisColor_gridColor_(
        self,
        frame,
        values,
        max_value,
        min_value,
        color,
        spacing,
        corner_radius,
        show_axes,
        show_grid,
        x_labels,
        y_labels,
        axis_color,
        grid_color,
    ):
        self = objc.super(_BarChartView, self).initWithFrame_(frame)
        if not self:
            return None

        self._values = list(values)
        self._max_value = float(max_value)
        self._min_value = float(min_value)
        self._color = color
        self._spacing = float(spacing)
        self._corner_radius = float(corner_radius)
        self._show_axes = show_axes
        self._show_grid = show_grid
        self._x_labels = list(x_labels) if x_labels else []
        self._y_labels = list(y_labels) if y_labels else []
        self._axis_color = axis_color
        self._grid_color = grid_color
        self.setWantsLayer_(True)

        return self

    def drawRect_(self, dirty_rect):
        """Draw the bar chart."""
        bounds = self.bounds()
        width = bounds.size.width
        height = bounds.size.height

        if len(self._values) == 0:
            return

        # Calculate chart area (reserve space for axes if needed)
        margin_left = 20.0 if self._show_axes and self._y_labels else 0.0
        margin_bottom = 10.0 if self._show_axes and self._x_labels else 0.0
        chart_width = width - margin_left
        chart_height = height - margin_bottom

        # Draw grid if enabled
        if self._show_grid:
            self._grid_color.setStroke()
            grid_path = NSBezierPath.bezierPath()
            grid_path.setLineWidth_(0.5)

            # Vertical grid lines (one for each bar)
            num_bars = len(self._values)
            for i in range(num_bars + 1):
                x = margin_left + (chart_width / num_bars * i)
                grid_path.moveToPoint_(NSMakePoint(x, margin_bottom))
                grid_path.lineToPoint_(NSMakePoint(x, height))

            # Horizontal grid lines (for y_labels)
            if self._y_labels:
                num_y_lines = len(self._y_labels)
                for i in range(num_y_lines):
                    y = margin_bottom + (
                        chart_height / (num_y_lines - 1) * i
                        if num_y_lines > 1
                        else chart_height / 2
                    )
                    grid_path.moveToPoint_(NSMakePoint(margin_left, y))
                    grid_path.lineToPoint_(NSMakePoint(width, y))

            grid_path.stroke()

        # Draw axes if enabled
        if self._show_axes:
            self._axis_color.setStroke()
            axis_path = NSBezierPath.bezierPath()
            axis_path.setLineWidth_(1.0)

            # Y-axis (left)
            axis_path.moveToPoint_(NSMakePoint(margin_left, margin_bottom))
            axis_path.lineToPoint_(NSMakePoint(margin_left, height))

            # X-axis (bottom)
            axis_path.moveToPoint_(NSMakePoint(margin_left, margin_bottom))
            axis_path.lineToPoint_(NSMakePoint(width, margin_bottom))

            axis_path.stroke()

            # Draw axis labels
            font = NSFont.systemFontOfSize_(8.0)
            attrs = {
                AppKit.NSFontAttributeName: font,
                AppKit.NSForegroundColorAttributeName: self._axis_color,
            }

            # X-axis labels
            if self._x_labels:
                num_x_labels = min(len(self._x_labels), len(self._values))
                for i in range(num_x_labels):
                    # Center label under each bar
                    total_spacing = self._spacing * (len(self._values) - 1)
                    bar_width = (chart_width - total_spacing) / len(self._values)
                    x = margin_left + i * (bar_width + self._spacing) + bar_width / 2

                    # Create NSAttributedString
                    label_str = Foundation.NSString.stringWithString_(
                        str(self._x_labels[i])
                    )
                    attr_string = (
                        AppKit.NSAttributedString.alloc().initWithString_attributes_(
                            label_str, attrs
                        )
                    )
                    label_size = attr_string.size()

                    label_rect = NSMakeRect(
                        x - label_size.width / 2,
                        margin_bottom - label_size.height - 2,
                        label_size.width,
                        label_size.height,
                    )
                    attr_string.drawInRect_(label_rect)

            # Y-axis labels
            if self._y_labels:
                num_y_labels = len(self._y_labels)
                for i, label in enumerate(self._y_labels):
                    y = margin_bottom + (
                        chart_height / (num_y_labels - 1) * i
                        if num_y_labels > 1
                        else chart_height / 2
                    )

                    # Create NSAttributedString
                    label_str = Foundation.NSString.stringWithString_(str(label))
                    attr_string = (
                        AppKit.NSAttributedString.alloc().initWithString_attributes_(
                            label_str, attrs
                        )
                    )
                    label_size = attr_string.size()

                    label_rect = NSMakeRect(
                        margin_left - label_size.width - 4,
                        y - label_size.height / 2,
                        label_size.width,
                        label_size.height,
                    )
                    attr_string.drawInRect_(label_rect)

        # Calculate bar width
        total_spacing = self._spacing * (len(self._values) - 1)
        bar_width = (chart_width - total_spacing) / len(self._values)

        # Draw each bar
        for i, value in enumerate(self._values):
            # Normalize value to height
            normalized = (value - self._min_value) / (self._max_value - self._min_value)
            bar_height = max(0, min(chart_height, normalized * chart_height))

            # Calculate position (offset by margins)
            x = margin_left + i * (bar_width + self._spacing)
            y = margin_bottom

            # Create rounded rect
            rect = NSMakeRect(x, y, bar_width, bar_height)
            path = NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(
                rect, self._corner_radius, self._corner_radius
            )

            # Fill bar
            self._color.setFill()
            path.fill()


def ring_chart(
    data=None,
    dimensions=(100, 100),
    colors=None,
    ring_width=10.0,
    spacing=2.0,
    labels=None,
):
    """Create a ring chart (multi-ring donut chart) using NSView drawing.

    Args:
        data: List of values for each ring (outer to inner). Each value is displayed as a percentage.
        dimensions: Tuple of (width, height) in points
        colors: List of colors for each ring (hex strings or NSColor). If None, uses default palette.
        ring_width: Width of each ring in points
        spacing: Space between rings in points
        labels: Optional list of label strings for each ring (displayed in legend)

    Returns:
        NSView containing the ring chart

    Example:
        ring_chart(
            data=[85, 65, 45, 25],
            colors=["#FFD60A", "#FF9F0A", "#FF453A", "#BF5AF2"],
            labels=["Ring 1", "Ring 2", "Ring 3", "Ring 4"]
        )
    """
    if data is None:
        data = []

    width, height = dimensions

    # Create container view
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)
    container.setWantsLayer_(True)

    container.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    container.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    if len(data) == 0:
        return container

    # Default colors if not provided
    if colors is None:
        colors = [
            "#FFD60A",  # Yellow
            "#FF9F0A",  # Orange
            "#FF453A",  # Red
            "#BF5AF2",  # Purple
            "#5E5CE6",  # Indigo
            "#32ADE6",  # Blue
            "#30D158",  # Green
        ]

    # Parse colors
    parsed_colors = [
        parse_color(color, default=NSColor.labelColor())
        for color in colors[: len(data)]
    ]

    # Pad with default colors if needed
    while len(parsed_colors) < len(data):
        parsed_colors.append(NSColor.labelColor())

    # Create ring chart view
    chart_view = (
        _RingChartView.alloc().initWithFrame_data_colors_ringWidth_spacing_labels_(
            NSMakeRect(0, 0, width, height),
            data,
            parsed_colors,
            ring_width,
            spacing,
            labels,
        )
    )

    container.addSubview_(chart_view)

    return container


class _RingChartView(NSView):
    """Custom view for rendering ring charts."""

    def initWithFrame_data_colors_ringWidth_spacing_labels_(
        self, frame, data, colors, ring_width, spacing, labels
    ):
        self = objc.super(_RingChartView, self).initWithFrame_(frame)
        if not self:
            return None

        self._data = list(data)
        self._colors = list(colors)
        self._ring_width = float(ring_width)
        self._spacing = float(spacing)
        self._labels = labels if labels else []
        self.setWantsLayer_(True)

        return self

    def drawRect_(self, dirty_rect):
        """Draw the ring chart."""
        bounds = self.bounds()
        width = bounds.size.width
        height = bounds.size.height

        if len(self._data) == 0:
            return

        # Calculate center and maximum radius
        center_x = width / 2.0
        center_y = height / 2.0
        max_radius = min(center_x, center_y)

        # Draw rings from outside to inside
        num_rings = len(self._data)
        for i, (value, color) in enumerate(zip(self._data, self._colors)):
            # Calculate radius for this ring
            outer_radius = max_radius - (i * (self._ring_width + self._spacing))
            inner_radius = outer_radius - self._ring_width

            if inner_radius < 0:
                break

            # Normalize value to percentage (0-100)
            percentage = max(0, min(100, float(value))) / 100.0

            # Draw background ring (unfilled portion)
            background_path = NSBezierPath.alloc().init()
            background_path.appendBezierPathWithArcWithCenter_radius_startAngle_endAngle_clockwise_(
                NSMakePoint(center_x, center_y),
                (outer_radius + inner_radius) / 2.0,
                0,
                360,
                False,
            )
            background_path.setLineWidth_(self._ring_width)

            # Use a lighter version of the color for background
            bg_color = color.colorWithAlphaComponent_(0.2)
            bg_color.setStroke()
            background_path.stroke()

            # Draw filled portion (arc representing the value)
            if percentage > 0:
                # Start from top (90 degrees) and go clockwise
                start_angle = 90
                end_angle = start_angle - (360 * percentage)

                filled_path = NSBezierPath.alloc().init()
                filled_path.appendBezierPathWithArcWithCenter_radius_startAngle_endAngle_clockwise_(
                    NSMakePoint(center_x, center_y),
                    (outer_radius + inner_radius) / 2.0,
                    start_angle,
                    end_angle,
                    True,  # Clockwise
                )
                filled_path.setLineWidth_(self._ring_width)
                filled_path.setLineCapStyle_(1)  # Round cap

                color.setStroke()
                filled_path.stroke()


def video(
    url,
    dimensions=(320, 240),
    show_controls=True,
    autoplay=False,
    loop=False,
    border_radius=None,
):
    """Create a video player using AVKit.

    Args:
        url: Video URL (string path to local file or remote URL)
        dimensions: Tuple of (width, height) in points
        show_controls: Whether to show playback controls (default: True)
        autoplay: Whether to start playing automatically (default: False)
        loop: Whether to loop the video (default: False)
        border_radius: Optional corner radius in points (e.g., 8.0 for rounded corners)

    Returns:
        NSView containing AVPlayerView with video player

    Note:
        Requires macOS 10.10+. Returns empty view if AVKit is not available.
    """
    if not AVKIT_AVAILABLE:
        print("AVKit is not available. Video control requires macOS 10.10+")
        return NSView.alloc().init()

    width, height = dimensions

    # Create container view
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)
    container.setWantsLayer_(True)

    # Set size constraints
    container.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    container.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    try:
        # Convert URL string to NSURL
        if isinstance(url, str):
            if url.startswith("http://") or url.startswith("https://"):
                ns_url = NSURL.URLWithString_(url)
            else:
                # Local file path
                ns_url = NSURL.fileURLWithPath_(url)
        else:
            ns_url = url

        # Create AVPlayer with the video URL
        player = AVFoundation.AVPlayer.playerWithURL_(ns_url)

        # Create AVPlayerView
        player_view = AVKit.AVPlayerView.alloc().initWithFrame_(
            NSMakeRect(0, 0, width, height)
        )
        player_view.setPlayer_(player)
        player_view.setControlsStyle_(
            AVKit.AVPlayerViewControlsStyleDefault
            if show_controls
            else AVKit.AVPlayerViewControlsStyleNone
        )
        player_view.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Apply border radius if specified
        if border_radius is not None:
            player_view.setWantsLayer_(True)
            player_view.layer().setCornerRadius_(border_radius)
            player_view.layer().setMasksToBounds_(True)

        # Add to container
        container.addSubview_(player_view)

        # Pin player view to container edges
        player_view.topAnchor().constraintEqualToAnchor_(
            container.topAnchor()
        ).setActive_(True)
        player_view.bottomAnchor().constraintEqualToAnchor_(
            container.bottomAnchor()
        ).setActive_(True)
        player_view.leadingAnchor().constraintEqualToAnchor_(
            container.leadingAnchor()
        ).setActive_(True)
        player_view.trailingAnchor().constraintEqualToAnchor_(
            container.trailingAnchor()
        ).setActive_(True)

        # Handle looping if requested
        if loop:
            # Set up notification observer for when video ends
            from Foundation import NSNotificationCenter

            class VideoLoopHandler(NSObject):
                def initWithPlayer_(self, player):
                    self = objc.super(VideoLoopHandler, self).init()
                    if not self:
                        return None
                    self.player = player
                    return self

                def playerDidFinishPlaying_(self, notification):
                    """Restart video when it finishes"""
                    self.player.seekToTime_completionHandler_(
                        AVFoundation.CMTimeMake(0, 1),
                        lambda finished: self.player.play() if finished else None,
                    )

            # Create loop handler and register for notifications
            loop_handler = VideoLoopHandler.alloc().initWithPlayer_(player)
            NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
                loop_handler,
                "playerDidFinishPlaying:",
                AVFoundation.AVPlayerItemDidPlayToEndTimeNotification,
                player.currentItem(),
            )

            # Keep reference to prevent garbage collection
            _delegate_registry[id(player_view)] = loop_handler

        # Autoplay if requested
        if autoplay:
            player.play()

        return container

    except Exception as e:
        print(f"Error creating video player: {e}")
        # Return empty view on error
        error_label = label(f"Video load error", font_size=10, color="gray")
        container.addSubview_(error_label)
        error_label.centerXAnchor().constraintEqualToAnchor_(
            container.centerXAnchor()
        ).setActive_(True)
        error_label.centerYAnchor().constraintEqualToAnchor_(
            container.centerYAnchor()
        ).setActive_(True)
        return container


def map_view(
    latitude=37.7749,
    longitude=-122.4194,
    zoom=0.05,
    dimensions=(320, 240),
    map_type="standard",
    show_controls=True,
    annotations=None,
    border_radius=None,
):
    """Create a map view using MapKit.

    Args:
        latitude: Center latitude coordinate (default: San Francisco)
        longitude: Center longitude coordinate (default: San Francisco)
        zoom: Zoom level as coordinate span in degrees (smaller = more zoomed in, default: 0.05)
        dimensions: Tuple of (width, height) in points
        map_type: Map type - "standard", "satellite", "hybrid", "satellite_flyover", "hybrid_flyover", "muted_standard" (default: "standard")
        show_controls: Whether to show zoom and compass controls (default: True)
        annotations: List of annotation dicts with keys: 'latitude', 'longitude', 'title', 'subtitle' (optional)
        border_radius: Optional corner radius in points (e.g., 8.0 for rounded corners)

    Returns:
        NSView containing MKMapView

    Note:
        Requires macOS 10.9+. Returns empty view if MapKit is not available.
    """
    if not MAPKIT_AVAILABLE:
        print("MapKit is not available. Map control requires macOS 10.9+")
        return NSView.alloc().init()

    width, height = dimensions

    # Create container view
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)
    container.setWantsLayer_(True)

    # Set size constraints
    container.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    container.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    try:
        # Create MKMapView
        map_view = MapKit.MKMapView.alloc().initWithFrame_(
            NSMakeRect(0, 0, width, height)
        )
        map_view.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Set map type
        map_type_dict = {
            "standard": MapKit.MKMapTypeStandard,
            "satellite": MapKit.MKMapTypeSatellite,
            "hybrid": MapKit.MKMapTypeHybrid,
        }

        # Handle newer map types with version check
        if hasattr(MapKit, "MKMapTypeSatelliteFlyover"):
            map_type_dict["satellite_flyover"] = MapKit.MKMapTypeSatelliteFlyover
        if hasattr(MapKit, "MKMapTypeHybridFlyover"):
            map_type_dict["hybrid_flyover"] = MapKit.MKMapTypeHybridFlyover
        if hasattr(MapKit, "MKMapTypeMutedStandard"):
            map_type_dict["muted_standard"] = MapKit.MKMapTypeMutedStandard

        map_view.setMapType_(map_type_dict.get(map_type, MapKit.MKMapTypeStandard))

        # Set center coordinate and zoom level
        center = MapKit.CLLocationCoordinate2D()
        center.latitude = latitude
        center.longitude = longitude

        span = MapKit.MKCoordinateSpan()
        span.latitudeDelta = zoom
        span.longitudeDelta = zoom

        region = MapKit.MKCoordinateRegion()
        region.center = center
        region.span = span

        map_view.setRegion_animated_(region, False)

        # Configure controls
        map_view.setZoomEnabled_(show_controls)
        map_view.setScrollEnabled_(show_controls)
        map_view.setRotateEnabled_(show_controls)

        # Show compass and zoom controls if available (macOS 10.13+)
        if hasattr(map_view, "setShowsCompass_"):
            map_view.setShowsCompass_(show_controls)
        if hasattr(map_view, "setShowsZoomControls_"):
            map_view.setShowsZoomControls_(show_controls)

        # Add annotations if provided
        if annotations:
            for ann_data in annotations:
                if isinstance(ann_data, dict):
                    ann_lat = ann_data.get("latitude", latitude)
                    ann_lon = ann_data.get("longitude", longitude)
                    ann_title = ann_data.get("title", "")
                    ann_subtitle = ann_data.get("subtitle", "")

                    annotation = MapKit.MKPointAnnotation.alloc().init()
                    coord = MapKit.CLLocationCoordinate2D()
                    coord.latitude = ann_lat
                    coord.longitude = ann_lon
                    annotation.setCoordinate_(coord)

                    if ann_title:
                        annotation.setTitle_(str(ann_title))
                    if ann_subtitle:
                        annotation.setSubtitle_(str(ann_subtitle))

                    map_view.addAnnotation_(annotation)

        # Apply border radius if specified
        if border_radius is not None:
            map_view.setWantsLayer_(True)
            map_view.layer().setCornerRadius_(border_radius)
            map_view.layer().setMasksToBounds_(True)

        # Add to container
        container.addSubview_(map_view)

        # Pin map view to container edges
        map_view.topAnchor().constraintEqualToAnchor_(container.topAnchor()).setActive_(
            True
        )
        map_view.bottomAnchor().constraintEqualToAnchor_(
            container.bottomAnchor()
        ).setActive_(True)
        map_view.leadingAnchor().constraintEqualToAnchor_(
            container.leadingAnchor()
        ).setActive_(True)
        map_view.trailingAnchor().constraintEqualToAnchor_(
            container.trailingAnchor()
        ).setActive_(True)

        return container

    except Exception as e:
        print(f"Error creating map view: {e}")
        # Return empty view on error
        error_label = label(f"Map load error", font_size=10, color="gray")
        container.addSubview_(error_label)
        error_label.centerXAnchor().constraintEqualToAnchor_(
            container.centerXAnchor()
        ).setActive_(True)
        error_label.centerYAnchor().constraintEqualToAnchor_(
            container.centerYAnchor()
        ).setActive_(True)
        return container


def web_view(
    url=None,
    html=None,
    dimensions=(400, 300),
    enable_javascript=True,
    transparent=False,
    border_radius=None,
    private_mode=True,
    storage_path=None,
):
    """Create a web view using WebKit.

    Args:
        url: URL to load (string). Takes precedence over html parameter.
        html: HTML string to load (optional, used if url is None)
        dimensions: Tuple of (width, height) in points
        enable_javascript: Whether to enable JavaScript (default: True)
        transparent: Whether to use transparent background (default: False)
        border_radius: Optional corner radius in points (e.g., 8.0 for rounded corners)
        private_mode: If True, cookies and persistent storage are not saved between sessions (default: True)
        storage_path (Optional[str]): Optional identifier for persistent storage.
            Only used if `private_mode` is False. Creates a unique WebKit data store
            in ``/Library/WebKit/com.stackit.webkit.<hash>/``. Requires macOS 13.3+
            for custom identifiers; falls back to the default storage on older versions.

    Returns:
        NSView containing WKWebView

    Note:
        Requires macOS 10.10+. Returns empty view if WebKit is not available.
        Either url or html must be provided.
    """
    if not WEBKIT_AVAILABLE:
        print("WebKit is not available. Web view control requires macOS 10.10+")
        return NSView.alloc().init()

    width, height = dimensions

    # Create container view
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)
    container.setWantsLayer_(True)

    # Set size constraints
    container.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    container.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    try:
        # Create WKWebView configuration
        config = WebKit.WKWebViewConfiguration.alloc().init()

        # Configure data store based on private_mode
        if private_mode:
            # Use non-persistent (ephemeral) data store - nothing saved between sessions
            config.setWebsiteDataStore_(
                WebKit.WKWebsiteDataStore.nonPersistentDataStore()
            )
        else:
            # Use persistent data store
            if storage_path:
                # Custom storage path
                import os

                identifier = f"com.stackit.webkit.{abs(hash(storage_path))}"

                # Check if initWithIdentifier_ is available (macOS 13.3+)
                if hasattr(WebKit.WKWebsiteDataStore, "alloc") and hasattr(
                    WebKit.WKWebsiteDataStore.alloc(), "initWithIdentifier_"
                ):
                    try:
                        data_store = (
                            WebKit.WKWebsiteDataStore.alloc().initWithIdentifier_(
                                identifier
                            )
                        )
                        config.setWebsiteDataStore_(data_store)
                    except Exception as e:
                        print(
                            f"Warning: Could not create custom data store: {e}. Using default."
                        )
                        config.setWebsiteDataStore_(
                            WebKit.WKWebsiteDataStore.defaultDataStore()
                        )
                else:
                    # Fallback for older macOS versions
                    print(
                        "Note: Custom storage identifiers require macOS 13.3+. "
                        "Using default storage."
                    )
                    config.setWebsiteDataStore_(
                        WebKit.WKWebsiteDataStore.defaultDataStore()
                    )

            else:
                # Use default persistent data store
                config.setWebsiteDataStore_(
                    WebKit.WKWebsiteDataStore.defaultDataStore()
                )

        # Configure JavaScript
        preferences = WebKit.WKPreferences.alloc().init()
        preferences.setJavaScriptEnabled_(enable_javascript)
        config.setPreferences_(preferences)

        # Create WKWebView
        web_view = WebKit.WKWebView.alloc().initWithFrame_configuration_(
            NSMakeRect(0, 0, width, height), config
        )
        web_view.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Enable layer for both transparency and border radius
        web_view.setWantsLayer_(True)

        # Set transparent background if requested
        if transparent:
            # Make the web view itself transparent
            web_view.setOpaque_(False)
            web_view.setValue_forKey_(NSColor.clearColor(), "backgroundColor")

            # Set layer to transparent
            web_view.layer().setOpaque_(False)
            web_view.layer().setBackgroundColor_(NSColor.clearColor().CGColor())

            # Also make sure the underlying scroll view is transparent
            if hasattr(web_view, "scrollView"):
                web_view.scrollView().setDrawsBackground_(False)

        # Apply border radius if specified
        if border_radius is not None:
            web_view.layer().setCornerRadius_(border_radius)
            web_view.layer().setMasksToBounds_(True)

        # Load content
        if url:
            # Load from URL
            if isinstance(url, str):
                ns_url = NSURL.URLWithString_(url)
            else:
                ns_url = url
            request = Foundation.NSURLRequest.requestWithURL_(ns_url)
            web_view.loadRequest_(request)
        elif html:
            # Load HTML string
            web_view.loadHTMLString_baseURL_(html, None)
        else:
            # No content provided - load blank page
            web_view.loadHTMLString_baseURL_(
                "<html><body style='margin:0;padding:20px;font-family:system-ui;color:#888;'>No content loaded</body></html>",
                None,
            )

        # Add to container
        container.addSubview_(web_view)

        # Pin web view to container edges
        web_view.topAnchor().constraintEqualToAnchor_(container.topAnchor()).setActive_(
            True
        )
        web_view.bottomAnchor().constraintEqualToAnchor_(
            container.bottomAnchor()
        ).setActive_(True)
        web_view.leadingAnchor().constraintEqualToAnchor_(
            container.leadingAnchor()
        ).setActive_(True)
        web_view.trailingAnchor().constraintEqualToAnchor_(
            container.trailingAnchor()
        ).setActive_(True)

        return container

    except Exception as e:
        print(f"Error creating web view: {e}")
        import traceback

        traceback.print_exc()
        # Return empty view on error
        error_label = label(f"Web view load error", font_size=10, color="gray")
        container.addSubview_(error_label)
        error_label.centerXAnchor().constraintEqualToAnchor_(
            container.centerXAnchor()
        ).setActive_(True)
        error_label.centerYAnchor().constraintEqualToAnchor_(
            container.centerYAnchor()
        ).setActive_(True)
        return container
