#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Progress StackIt Controls.

This module provides progress controls like progress bars and circular progress indicators
for showing task completion or activity status.
"""

from ._base import *


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