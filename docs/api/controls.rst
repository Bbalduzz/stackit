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

Image Controls
--------------

image()
~~~~~~~

Create an image view.

.. code-block:: python

   # From file path
   img = stackit.image("/path/to/image.png", width=24, height=24)

   # From SF Symbol
   symbol = stackit.SFSymbol.create("star.fill")
   img = stackit.image(symbol, width=24, height=24)

   # From URL
   img = stackit.image("https://example.com/image.png", width=100, height=100)

**Parameters:**

* ``image_source`` (str or NSImage) - Path, URL, or NSImage object
* ``width`` (int) - Image width (default: 24)
* ``height`` (int) - Image height (default: 24)
* ``scaling`` (int) - NSImageScaling mode (optional)
