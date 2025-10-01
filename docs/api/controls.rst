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

Create a radio button.

.. code-block:: python

   radio = stackit.radio_button("Option 1", state=False)

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

**Parameters:**

* ``points`` (list) - List of data points to plot
* ``dimensions`` (tuple) - Chart dimensions as (width, height) in points (default: (60, 20))
* ``max_value`` (float) - Maximum value for y-axis scaling (default: 100.0)
* ``min_value`` (float) - Minimum value for y-axis scaling (default: 0.0)
* ``color`` (str or NSColor) - Line color (default: system label color)
* ``line_width`` (float) - Width of the line stroke (default: 0.5)
* ``fill`` (bool) - Whether to fill area under the line (default: True)

**Note:** Uses SpriteKit's SKKeyframeSequence for smooth spline interpolation. Falls back to linear interpolation if SpriteKit is unavailable.

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
