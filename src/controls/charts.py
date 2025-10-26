#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chart Controls - Line charts, bar charts, and ring charts.

This module provides chart visualization controls for creating
interactive data visualizations in menu bar applications.
"""

from ._base import *


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
