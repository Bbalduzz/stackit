Controls Module
===============

The controls module provides standalone functions for creating UI controls.

Text Controls
-------------

label()
~~~~~~~

Create a text label.

.. code-block:: python

   label = stackit.label("Hello World", font_size=14, bold=True, color="blue")

**Parameters:**

* ``text`` (str) - The label text
* ``font_size`` (int) - Font size in points (default: 13)
* ``bold`` (bool) - Whether to use bold font (default: False)
* ``color`` (str or NSColor) - Text color (default: system color)

link()
~~~~~~

Create a clickable hyperlink.

.. code-block:: python

   link = stackit.link("Visit Site", url="https://example.com", font_size=13)

**Parameters:**

* ``text`` (str) - The link text
* ``url`` (str) - The URL to open when clicked
* ``font_size`` (int) - Font size in points (default: 13)

Input Controls
--------------

text_field()
~~~~~~~~~~~~

Create a text input field.

.. code-block:: python

   field = stackit.text_field(width=200, placeholder="Enter text", font_size=13)

**Parameters:**

* ``width`` (int) - Field width in pixels (default: 200)
* ``placeholder`` (str) - Placeholder text (optional)
* ``font_size`` (int) - Font size (default: 13)

secure_text_input()
~~~~~~~~~~~~~~~~~~~

Create a secure text input field (for passwords).

.. code-block:: python

   password = stackit.secure_text_input(width=200, placeholder="Password")

search_field()
~~~~~~~~~~~~~~

Create a search input field with search icon.

.. code-block:: python

   search = stackit.search_field(width=200, placeholder="Search...")

Button Controls
---------------

button()
~~~~~~~~

Create a clickable button.

.. code-block:: python

   btn = stackit.button("Click Me", target=self, action="buttonClicked:")

**Parameters:**

* ``title`` (str) - Button text
* ``target`` (object) - Target object for action (optional)
* ``action`` (str) - Selector string for action (optional)

checkbox()
~~~~~~~~~~

Create a checkbox control.

.. code-block:: python

   checkbox = stackit.checkbox("Enable feature", state=True)

**Parameters:**

* ``title`` (str) - Checkbox label
* ``state`` (bool) - Initial checked state (default: False)

radio_button()
~~~~~~~~~~~~~~

Create a single radio button.

.. code-block:: python

   radio = stackit.radio_button("Option 1", state=False)

**Note:** For proper mutually exclusive radio button groups, use ``radio_group()`` instead.

radio_group()
~~~~~~~~~~~~~

Create a group of mutually exclusive radio buttons.

.. code-block:: python

   # Simple string labels (default)
   def handle_selection(sender):
       print(f"Selected: {sender.title()}")

   group = stackit.radio_group(
       options=["Small", "Medium", "Large"],
       selected=1,  # Medium is initially selected
       callback=handle_selection
   )

   # Horizontal radio group
   color_group = stackit.radio_group(
       options=["Red", "Green", "Blue"],
       selected=0,
       orientation="horizontal",
       spacing=12.0
   )

   # Pre-configured radio buttons for more control
   custom_group = stackit.radio_group(
       options=[
           stackit.radio_button("Option A"),
           stackit.radio_button("Option B"),
           stackit.radio_button("Option C")
       ],
       selected=0,
       callback=handle_selection
   )

**Parameters:**

* ``options`` (list[str] or list[NSButton]) - List of radio button labels (strings) or pre-configured radio buttons
* ``selected`` (int) - Index of initially selected option (default: 0)
* ``orientation`` (str) - Layout orientation: "vertical" or "horizontal" (default: "vertical")
* ``spacing`` (float) - Spacing between buttons in points (default: 8.0)
* ``callback`` (callable) - Function called when selection changes, receives the selected NSButton
* ``**kwargs`` - Additional attributes (only applied when options are strings)

**Returns:** StackView containing the radio button group with mutual exclusivity

Progress Controls
-----------------

progress_bar()
~~~~~~~~~~~~~~

Create a horizontal progress bar.

.. code-block:: python

   progress = stackit.progress_bar(width=200, value=0.5, indeterminate=False)

**Parameters:**

* ``width`` (int) - Bar width in pixels (default: 200)
* ``value`` (float) - Progress value 0.0-1.0 (default: 0.0)
* ``indeterminate`` (bool) - Show indeterminate animation (default: False)

circular_progress()
~~~~~~~~~~~~~~~~~~~

Create a circular progress indicator (spinner).

.. code-block:: python

   spinner = stackit.circular_progress(size=16, indeterminate=True)

**Parameters:**

* ``size`` (int) - Diameter in pixels (default: 32)
* ``indeterminate`` (bool) - Show indeterminate animation (default: True)

Slider Controls
---------------

slider()
~~~~~~~~

Create a horizontal slider.

.. code-block:: python

   slider = stackit.slider(width=150, min_value=0, max_value=100, value=50)

**Parameters:**

* ``width`` (int) - Slider width in pixels (default: 150)
* ``min_value`` (float) - Minimum value (default: 0)
* ``max_value`` (float) - Maximum value (default: 100)
* ``value`` (float) - Initial value (default: 50)

Selection Controls
------------------

combobox()
~~~~~~~~~~

Create a combo box (dropdown menu).

.. code-block:: python

   combo = stackit.combobox(
       items=["Option 1", "Option 2", "Option 3"],
       width=200,
       editable=False
   )

**Parameters:**

* ``items`` (list) - List of string items
* ``width`` (int) - Width in pixels (default: 200)
* ``editable`` (bool) - Allow text editing (default: False)

Date and Time Controls
----------------------

date_picker()
~~~~~~~~~~~~~

Create a date picker control.

.. code-block:: python

   picker = stackit.date_picker(
       date=datetime.now(),
       date_only=True,
       width=200
   )

**Parameters:**

* ``date`` (datetime) - Initial date (default: now)
* ``date_only`` (bool) - Show only date, not time (default: True)
* ``width`` (int) - Width in pixels (default: 200)

time_picker()
~~~~~~~~~~~~~

Create a time picker control.

.. code-block:: python

   picker = stackit.time_picker(
       time=datetime.now(),
       width=150
   )

**Parameters:**

* ``time`` (datetime) - Initial time (default: now)
* ``width`` (int) - Width in pixels (default: 150)

Layout Controls
---------------

spacer()
~~~~~~~~

Create a flexible spacer that expands to fill available space.

.. code-block:: python

   spacer = stackit.spacer(priority=250)

**Parameters:**

* ``priority`` (int) - Hugging priority (default: 250). Lower = more expansion.

separator()
~~~~~~~~~~~

Create a horizontal separator line.

.. code-block:: python

   sep = stackit.separator(width=200)

**Parameters:**

* ``width`` (int) - Separator width in pixels (default: 200)

Layout Containers
-----------------

block()
~~~~~~~

Create a bordered and rounded container around content (similar to SwiftUI's menuBlock modifier).

.. code-block:: python

   # Wrap content in a block
   content = stackit.vstack([
       stackit.label("Network", bold=True),
       stackit.label("Status: Active")
   ])

   block = stackit.block(content, radius=8.0, padding=12.0)

   # Custom colors
   custom_block = stackit.block(
       content,
       radius=10.0,
       padding=16.0,
       border_color="#FF990080",
       background_color="#FF990020"
   )

**Parameters:**

* ``content_view`` (NSView) - The view to wrap (StackView or any NSView)
* ``radius`` (float) - Corner radius in points (default: 8.0)
* ``padding`` (float or tuple) - Padding around content, single value or (top, leading, bottom, trailing) (default: 12.0)
* ``border_color`` (str or NSColor) - Border color as hex string or NSColor (default: subtle gray)
* ``background_color`` (str or NSColor) - Background color as hex string or NSColor (default: subtle white)

**Note:** Creates a subtle shadow for depth and uses transparency for a native macOS look.

Chart Controls
--------------

line_chart()
~~~~~~~~~~~~

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
~~~~~~~~~~~

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
~~~~~~~~~~~~

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

Image Controls
--------------

image()
~~~~~~~

Create an image view with optional rounded corners.

.. code-block:: python

   # From SF Symbol
   symbol = stackit.SFSymbol("star.fill", color="#FFD700")
   img = stackit.image(symbol, width=24, height=24)

   # From URL
   img = stackit.image("https://example.com/image.png", width=100, height=100)

   # With rounded corners
   img = stackit.image(
       "https://example.com/avatar.jpg",
       width=50,
       height=50,
       border_radius=8.0  # Rounded corners
   )

   # Circular image (border_radius = width/2)
   img = stackit.image(
       "https://example.com/avatar.jpg",
       width=50,
       height=50,
       border_radius=25.0  # Perfect circle
   )

**Parameters:**

* ``image_path`` (str or SFSymbol) - SFSymbol instance or URL string
* ``width`` (int) - Image width in pixels (optional)
* ``height`` (int) - Image height in pixels (optional)
* ``scaling`` (int) - NSImageScaling mode (optional)
* ``border_radius`` (float) - Corner radius in points for rounded corners (optional)

Media Controls
--------------

video()
~~~~~~~

Create a video player using AVKit.

.. code-block:: python

   # Basic video player
   player = stackit.video(
       "https://example.com/video.mp4",
       dimensions=(400, 225),
       show_controls=True
   )

   # Local video file
   player = stackit.video(
       "/path/to/video.mp4",
       dimensions=(400, 225),
       autoplay=True,
       loop=True
   )

   # With rounded corners
   player = stackit.video(
       "video.mp4",
       dimensions=(400, 225),
       border_radius=12.0,
       show_controls=True
   )

**Parameters:**

* ``url`` (str) - Video URL (local file path or remote URL)
* ``dimensions`` (tuple) - Video player dimensions as (width, height) in points (default: (320, 240))
* ``show_controls`` (bool) - Whether to show playback controls (default: True)
* ``autoplay`` (bool) - Whether to start playing automatically (default: False)
* ``loop`` (bool) - Whether to loop the video (default: False)
* ``border_radius`` (float) - Corner radius in points for rounded corners (optional)

**Note:** Requires macOS 10.10+. Returns empty view if AVKit is not available.

map_view()
~~~~~~~~~~

Create an interactive map view using MapKit.

.. code-block:: python

   # Basic map
   map1 = stackit.map_view(
       latitude=37.7749,
       longitude=-122.4194,
       zoom=0.05,
       dimensions=(400, 300)
   )

   # Map with annotations
   map2 = stackit.map_view(
       latitude=40.7128,
       longitude=-74.0060,
       zoom=0.03,
       dimensions=(400, 300),
       map_type="satellite",
       annotations=[
           {
               'latitude': 40.7128,
               'longitude': -74.0060,
               'title': 'New York City',
               'subtitle': 'The Big Apple'
           }
       ]
   )

   # Hybrid map with rounded corners
   map3 = stackit.map_view(
       latitude=48.8566,
       longitude=2.3522,
       zoom=0.02,
       dimensions=(400, 300),
       map_type="hybrid",
       border_radius=12.0,
       show_controls=True
   )

**Parameters:**

* ``latitude`` (float) - Center latitude coordinate (default: 37.7749 - San Francisco)
* ``longitude`` (float) - Center longitude coordinate (default: -122.4194 - San Francisco)
* ``zoom`` (float) - Zoom level as coordinate span in degrees (smaller = more zoomed in, default: 0.05)
* ``dimensions`` (tuple) - Map view dimensions as (width, height) in points (default: (320, 240))
* ``map_type`` (str) - Map type: "standard", "satellite", "hybrid", "satellite_flyover", "hybrid_flyover", "muted_standard" (default: "standard")
* ``show_controls`` (bool) - Whether to show zoom, pan, and compass controls (default: True)
* ``annotations`` (list) - List of annotation dicts with keys: 'latitude', 'longitude', 'title', 'subtitle' (optional)
* ``border_radius`` (float) - Corner radius in points for rounded corners (optional)

**Note:** Requires macOS 10.9+. Returns empty view if MapKit is not available.

web_view()
~~~~~~~~~~

Create a web view using WebKit.

.. code-block:: python

   # Load a website
   web = stackit.web_view(
       "https://example.com",
       dimensions=(500, 400),
       border_radius=12.0
   )

   # Load local HTML file
   local_web = stackit.web_view(
       "file:///path/to/index.html",
       dimensions=(400, 300)
   )

   # Load custom HTML string
   html_content = """
   <!DOCTYPE html>
   <html>
   <head>
       <style>
           body { font-family: -apple-system; padding: 20px; }
           h1 { color: #0080FF; }
       </style>
   </head>
   <body>
       <h1>Custom Content</h1>
       <p>This is embedded HTML</p>
   </body>
   </html>
   """

   custom_web = stackit.web_view(
       html_content,
       dimensions=(400, 300),
       border_radius=8.0
   )

**Parameters:**

* ``url`` (str) - URL to load (can be http(s):// URL, file:// path, or raw HTML string)
* ``dimensions`` (tuple) - Web view dimensions as (width, height) in points (default: (320, 240))
* ``border_radius`` (float) - Corner radius in points for rounded corners (optional)

**Note:** Requires macOS 10.10+. Returns empty view if WebKit is not available. Automatically detects if input is a URL, file path, or HTML string.
