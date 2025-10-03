Text Controls
=============

label()
-------

Create a text label.

.. code-block:: python

   label = stackit.label("Hello World", font_size=14, bold=True, color="blue")

**Parameters:**

* ``text`` (str) - The label text
* ``font_size`` (int) - Font size in points (default: 13)
* ``bold`` (bool) - Whether to use bold font (default: False)
* ``color`` (str or NSColor) - Text color (default: system color)

link()
------

Create a clickable hyperlink.

.. code-block:: python

   link = stackit.link("Visit Site", url="https://example.com", font_size=13)

**Parameters:**

* ``text`` (str) - The link text
* ``url`` (str) - The URL to open when clicked
* ``font_size`` (int) - Font size in points (default: 13)
