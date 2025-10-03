Chart Controls
==============

line_chart()
------------

Create a line chart with smooth spline interpolation using SpriteKit.

.. code-block:: python

   # Simple line chart with default styling
   chart = stackit.line_chart(
       points=[10, 15, 8, 20, 18, 25, 22, 26, 24, 26],
       dimensions=(60, 20),
       max_value=100.0
   )

   # Customized line chart
   chart = stackit.line_chart(
       points=[5, 10, 8, 15, 20],
       dimensions=(100, 40),
       max_value=25.0,
       min_value=0.0,
       color="#FF0000",
       line_width=1.0,
       fill=True
   )

   # Line chart with axes and grid
   chart = stackit.line_chart(
       points=[45, 52, 48, 55, 62, 58, 65, 70, 68, 72],
       dimensions=(250, 120),
       max_value=100.0,
       color="#0A84FF",
       show_axes=True,
       show_grid=True,
       x_labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
       y_labels=[0, 25, 50, 75, 100]
   )

**Parameters:**

* ``points`` (list) - List of data points to plot
* ``dimensions`` (tuple) - Chart dimensions as (width, height) in points (default: (60, 20))
* ``max_value`` (float) - Maximum value for y-axis scaling (default: 100.0)
* ``min_value`` (float) - Minimum value for y-axis scaling (default: 0.0)
* ``color`` (str or NSColor) - Line color (default: system label color)
* ``line_width`` (float) - Width of the line stroke (default: 0.5)
* ``fill`` (bool) - Whether to fill area under the line (default: True)
* ``show_axes`` (bool) - Whether to show X and Y axes (default: False)
* ``show_grid`` (bool) - Whether to show grid lines (default: False)
* ``x_labels`` (list) - List of labels for X-axis tick marks (optional)
* ``y_labels`` (list) - List of labels for Y-axis tick marks (optional)
* ``axis_color`` (str or NSColor) - Color for axes and labels (default: secondary label color)
* ``grid_color`` (str or NSColor) - Color for grid lines (default: separator color)

**Note:** Uses SpriteKit's SKKeyframeSequence for smooth spline interpolation. Falls back to linear interpolation if SpriteKit is unavailable. When axes are enabled, chart automatically reserves 30px (left) and 20px (bottom) for axis labels.

bar_chart()
-----------

Create a bar chart using NSView drawing.

.. code-block:: python

   # Simple bar chart
   chart = stackit.bar_chart(
       values=[10, 25, 15, 30, 20],
       dimensions=(60, 20),
       max_value=50.0
   )

   # Customized bar chart
   chart = stackit.bar_chart(
       values=[5, 10, 8, 15, 12],
       dimensions=(100, 40),
       max_value=20.0,
       min_value=0.0,
       color="#00FF00",
       bar_spacing=2.0,
       corner_radius=2.0
   )

   # Bar chart with axes and grid
   chart = stackit.bar_chart(
       values=[65, 80, 55, 90, 70, 85, 75],
       dimensions=(250, 120),
       max_value=100.0,
       color="#32D74B",
       show_axes=True,
       show_grid=True,
       x_labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
       y_labels=[0, 50, 100]
   )

**Parameters:**

* ``values`` (list) - List of data values to plot
* ``dimensions`` (tuple) - Chart dimensions as (width, height) in points (default: (60, 20))
* ``max_value`` (float) - Maximum value for scaling (default: 100.0)
* ``min_value`` (float) - Minimum value for scaling (default: 0.0)
* ``color`` (str or NSColor) - Bar color (default: system green)
* ``bar_spacing`` (float) - Space between bars in points (default: 1.0)
* ``corner_radius`` (float) - Rounded corner radius for bars (default: 1.0)
* ``show_axes`` (bool) - Whether to show X and Y axes (default: False)
* ``show_grid`` (bool) - Whether to show grid lines (default: False)
* ``x_labels`` (list) - List of labels for X-axis tick marks (optional)
* ``y_labels`` (list) - List of labels for Y-axis tick marks (optional)
* ``axis_color`` (str or NSColor) - Color for axes and labels (default: secondary label color)
* ``grid_color`` (str or NSColor) - Color for grid lines (default: separator color)

**Note:** When axes are enabled, chart automatically reserves 30px (left) and 20px (bottom) for axis labels. X-axis labels are centered under each bar.

ring_chart()
------------

Create a multi-ring donut chart (activity rings style).

.. code-block:: python

   # Activity rings
   chart = stackit.ring_chart(
       data=[85, 65, 45, 25],  # Percentage values (0-100)
       dimensions=(120, 120),
       colors=["#FFD60A", "#FF9F0A", "#FF453A", "#BF5AF2"],
       ring_width=10.0,
       spacing=2.0
   )

   # Fitness-style progress rings
   fitness_rings = stackit.ring_chart(
       data=[90, 70, 50],
       dimensions=(100, 100),
       colors=["#32D74B", "#0A84FF", "#FF375F"],  # Move, Exercise, Stand
       ring_width=12.0,
       spacing=3.0,
       labels=["Move", "Exercise", "Stand"]
   )

**Parameters:**

* ``data`` (list) - List of percentage values (0-100) for each ring, outer to inner
* ``dimensions`` (tuple) - Chart dimensions as (width, height) in points (default: (100, 100))
* ``colors`` (list) - List of colors for each ring (hex strings or NSColor). Default palette: Yellow, Orange, Red, Purple, Indigo, Blue, Green
* ``ring_width`` (float) - Width of each ring in points (default: 10.0)
* ``spacing`` (float) - Space between rings in points (default: 2.0)
* ``labels`` (list) - Optional list of label strings for each ring (for future legend support)

**Note:** Background rings are displayed at 20% opacity. Rings are drawn from outside to inside.
