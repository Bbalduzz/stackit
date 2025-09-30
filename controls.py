#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
StackBar Controls - Standalone control creation functions.

This module provides standalone functions for creating UI controls that can be used
in StackMenuItem layouts without needing to reference the StackMenuItem instance.
"""

import Foundation
import AppKit
from Foundation import NSMakeRect, NSMakeSize, NSMakePoint, NSData
from AppKit import (
    NSObject, NSView, NSTextField, NSFont, NSColor, NSImageView, NSButton, NSSlider,
    NSProgressIndicator, NSComboBox, NSBezierPath, NSRoundLineCapStyle, NSTextView, NSScrollView, NSSize,
    NSApp, NSApplication, NSSecureTextField, NSKeyDown, NSCommandKeyMask,
    NSShiftKeyMask, NSControlKeyMask, NSDeviceIndependentModifierFlagsMask, NSSearchField, NSURL, NSDatePicker, NSTimeZone
)
import httpx
from .sfsymbol import SFSymbol

# Global registry to keep delegate references alive
_delegate_registry = {}
import objc
import datetime

class ScrollViewWithTextView(NSScrollView):
    def initWithSize_VScroll_(self, size: tuple[float, float], vscroll: bool):
        self = objc.super(ScrollViewWithTextView, self).initWithFrame_(NSMakeRect(0, 0, *size))
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
        return performKeyEquivalent_(self, event)


class SecureEditing(NSSecureTextField):
    """NSSecureTextField with cut, copy, paste, undo and selectAll

    Supports both Command (⌘) and Control (^) key combinations for cross-platform compatibility.
    Note: Copy is disabled for security reasons in secure text fields.
    """
    def performKeyEquivalent_(self, event):
        return performKeyEquivalent_(self, event)


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
        # Try our custom key handling first
        if performKeyEquivalent_(self, event):
            return True
        # Fall back to super implementation
        return objc.super(SearchFieldEditing, self).performKeyEquivalent_(event)

    def keyDown_(self, event):
        """Handle key down events directly for search field"""
        # Try our custom key handling first
        if performKeyEquivalent_(self, event):
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
        if NSApp.sendAction_to_from_(b"copy:", None, self):
            return
        objc.super(SearchFieldEditing, self).copy_(sender)

    def paste_(self, sender):
        """Handle paste action"""
        if NSApp.sendAction_to_from_(b"paste:", None, self):
            return
        objc.super(SearchFieldEditing, self).paste_(sender)

    def cut_(self, sender):
        """Handle cut action"""
        if NSApp.sendAction_to_from_(b"cut:", None, self):
            return
        objc.super(SearchFieldEditing, self).cut_(sender)


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

    def initWithText_fontSize_bold_color_maxLines_width_(self, text, font_size, bold, color, max_lines, width):
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


def label(text, font_size=13, bold=False, color=None, wraps=False, max_lines=0, width=None):
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

def image(image_path, width=None, height=None, scaling=None):
    """Create an image view from a network URL or SFSymbol.

    Args:
        image_path: SFSymbol instance or URL string (http:// or https://)
        width: Optional width constraint
        height: Optional height constraint
        scaling: Optional NSImageScaling constant

    Returns:
        NSImageView with the loaded image
    """
    try:
        image = None
        
        # Handle SFSymbol instances
        if isinstance(image_path, SFSymbol):
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
        elif isinstance(image_path, str) and (image_path.startswith('http://') or image_path.startswith('https://')):
            # Fetch image data with httpx
            with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                response = client.get(
                    image_path,
                    headers={'User-Agent': 'YourApp/1.0'}
                )
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
            image_view.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

        return image_view
        
    except Exception as e:
        print(f"Error loading image from {image_path}: {e}")
        return NSView.alloc().init()  # Return empty view on error


def button(title=None, target=None, action=None, style="default", image=None, image_position="left"):
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
        AppKit.NSLayoutConstraintOrientationHorizontal
    )
    button.setContentCompressionResistancePriority_forOrientation_(
        AppKit.NSLayoutPriorityDefaultHigh,
        AppKit.NSLayoutConstraintOrientationHorizontal
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
    spacer.setContentHuggingPriority_forOrientation_(priority, AppKit.NSLayoutConstraintOrientationHorizontal)
    spacer.setContentHuggingPriority_forOrientation_(priority, AppKit.NSLayoutConstraintOrientationVertical)
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


def progress_bar(value=0.0, indeterminate=False, dimensions=(200, 20), show_text=True, color=None):
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
            ns_color = _parse_color(color)
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


def circular_progress(value=0.0, indeterminate=False, dimensions=(40, 40), color=None, line_width=3.0):
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
        ns_color = _parse_color(color) if color else None

        custom_view = _create_circular_progress_view(
            NSMakeRect(2, 2, width - 4, height - 4),
            max(0.0, min(1.0, value)),
            ns_color,
            line_width
        )
        container.addSubview_(custom_view)

    return container


def _parse_color(color):
    """Parse color parameter into NSColor."""
    try:
        if isinstance(color, str) and color.startswith('#'):
            hex_color = color[1:]
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, 1.0)
        elif isinstance(color, (tuple, list)) and len(color) >= 3:
            r, g, b = color[:3]
            a = color[3] if len(color) > 3 else 1.0
            if any(val > 1.0 for val in [r, g, b]):
                r, g, b = r/255.0, g/255.0, b/255.0
            if a > 1.0:
                a = a/255.0
            return NSColor.colorWithRed_green_blue_alpha_(r, g, b, a)
    except Exception:
        pass
    return None


def _create_circular_progress_view(frame, value, color, line_width):
    """Create a custom circular progress view."""

    class CircularProgressView(NSView):

        def initWithFrame_value_color_lineWidth_(self, frame, value, color, line_width):
            self = objc.super(CircularProgressView, self).initWithFrame_(frame)
            if self:
                self._value = float(value) if value is not None else 0.0
                self._color = color or NSColor.colorWithSRGBRed_green_blue_alpha_(0x7F/255.0, 0x84/255.0, 0x8A/255.0, 1.0)
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
            track.appendBezierPathWithOvalInRect_(NSMakeRect(cx - radius, cy - radius, radius * 2, radius * 2))
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

    return CircularProgressView.alloc().initWithFrame_value_color_lineWidth_(frame, value, color, line_width)


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
        from AppKit import NSApp
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
    checkbox.setState_(AppKit.NSControlStateValueOn if checked else AppKit.NSControlStateValueOff)
    checkbox.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Set up callback using NSApp and StackAppDelegate
    if callback:
        from AppKit import NSApp
        from .delegate import StackAppDelegate
        checkbox.setTarget_(NSApp)
        checkbox.setAction_("checkboxCallback:")
        # Register callback with delegate
        StackAppDelegate.register_callback(checkbox, None, callback)

    return checkbox


def combobox(items=None, selected_index=-1, width=200, height=22, callback=None, editable=False):
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
        from AppKit import NSApp
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
    action = None,
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
    text_field.becomeFirstResponder()
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

def search_field(
    size: tuple[float, float] = (200, 25),
    target: NSObject | None = None,
    action = None,
    **kwargs,
) -> NSSearchField:
    """Create a search field.

    Args:
        size: width, height of the text field
        target: target to send action to
        action: action to send when the date is changed
        **kwargs: additional keyword/value attributes to configure

    Returns NSSearchField
    """
    search_field = NSSearchField.alloc().initWithFrame_(NSMakeRect(0, 0, *size))
    if target:
        search_field.setTarget_(target)
    if action:
        search_field.setAction_(action)
    if kwargs:
        for key, value in kwargs.items():
            method = f"set{key[0].upper()}{key[1:]}_"
            if hasattr(search_field, method):
                getattr(search_field, method)(value)

    return search_field

# def search_field(size: tuple[float, float] = (200, 25), target=None, action=None, placeholder=None, callback=None, **kwargs) -> NSSearchField:
#     """Create a search field with full keyboard shortcut support.

#     Args:
#         size: width, height of the text field
#         target: target to send action to (takes precedence over callback)
#         action: action to send when the search field is used
#         placeholder: placeholder text
#         callback: Python function to call when search field is used
#         **kwargs: additional keyword/value attributes to configure

#     Returns NSSearchField with copy/paste support
#     """
#     # Use the custom SearchFieldEditing class for keyboard shortcut support
#     search_field = SearchFieldEditing.alloc().initWithFrame_(NSMakeRect(0, 0, *size))

#     # Enable proper text editing behavior
#     search_field.setEditable_(True)
#     search_field.setSelectable_(True)
#     search_field.setTranslatesAutoresizingMaskIntoConstraints_(False)

#     # Enable standard text editing features
#     search_field.setImportsGraphics_(False)
#     search_field.setAllowsEditingTextAttributes_(False)

#     # Make sure the search field can become first responder
#     search_field.setRefusesFirstResponder_(False)

#     # Handle target/action vs callback
#     if target and action:
#         search_field.setTarget_(target)
#         search_field.setAction_(action)
#     elif callback:
#         from AppKit import NSApp
#         from .delegate import StackAppDelegate
#         search_field.setTarget_(NSApp)
#         search_field.setAction_("searchFieldCallback:")
#         # Register callback with delegate
#         StackAppDelegate.register_callback(search_field, None, callback)

#     if placeholder:
#         search_field.setPlaceholderString_(placeholder)

#     if kwargs:
#         for key, value in kwargs.items():
#             method = f"set{key[0].upper()}{key[1:]}_"
#             if hasattr(search_field, method):
#                 getattr(search_field, method)(value)

#     return search_field


def radio_button(title: str, target=None, action=None, callback=None, **kwargs) -> NSButton:
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
        from AppKit import NSApp
        from .delegate import StackAppDelegate
        radio_button = NSButton.buttonWithTitle_target_action_(title, NSApp, "radioButtonCallback:")
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


def date_picker(
    style: int = AppKit.NSDatePickerStyleClockAndCalendar,
    elements: int = AppKit.NSDatePickerElementFlagYearMonthDay,
    mode: int = AppKit.NSDatePickerModeSingle,
    date: datetime.date | datetime.datetime | None = None,
    target: NSObject | None = None,
    action = None,
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
        from AppKit import NSApp
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
    action = None,
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
