SFSymbol Module
===============

The SFSymbol module provides support for Apple's SF Symbols with extensive customization.

SFSymbol Class
--------------

SF Symbols are Apple's system-provided icons that adapt to appearance and accessibility settings.

Creating SF Symbols
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Basic symbol
   icon = stackit.SFSymbol("star.fill")

   # With point size and weight
   icon = stackit.SFSymbol("star.fill", point_size=20, weight="bold")

   # With color (hex or RGB tuple)
   icon = stackit.SFSymbol("heart.fill", color="#FF0000")
   icon = stackit.SFSymbol("heart.fill", color=(255, 0, 0))

   # With hierarchical rendering
   icon = stackit.SFSymbol(
       "gear",
       point_size=24,
       weight="semibold",
       rendering="hierarchical",
       color="#0000FF"
   )

   # Multicolor symbols
   icon = stackit.SFSymbol(
       "heart.circle.fill",
       point_size=32,
       rendering="multicolor"
   )

   # Palette mode with multiple colors
   icon = stackit.SFSymbol(
       "circle.hexagongrid.circle",
       point_size=24,
       rendering="palette",
       palette_colors=["#FF0000", "#00FF00", "#0000FF"]
   )

__init__()
~~~~~~~~~~

Create an SF Symbol image.

**Parameters:**

* ``name`` (str) - SF Symbol name (e.g., "star.fill", "heart", "gear")
* ``rendering`` (str) - Rendering mode: "automatic", "monochrome", "hierarchical", "palette", "multicolor" (default: "automatic")
* ``color`` (str or tuple) - Primary color as hex string "#FFFFFF" or RGB tuple (255, 255, 255) or RGBA (255, 255, 255, 255) (default: "#ffffff")
* ``palette_colors`` (list) - List of colors for palette mode (e.g., ["#FF0000", "#00FF00", "#0000FF"])
* ``point_size`` (float) - Point size for the symbol (optional)
* ``weight`` (str) - Font weight (default: None)
* ``scale`` (str) - Symbol scale: "small", "medium", "large" (optional)
* ``text_style`` (str) - Text style: "body", "caption1", "headline", "title1", etc. (optional)
* ``accessibility_description`` (str) - Accessibility description (default: auto-generated from name)

Weight Options
~~~~~~~~~~~~~~

* ``"ultraLight"``
* ``"thin"``
* ``"light"``
* ``"regular"`` (default)
* ``"medium"``
* ``"semibold"``
* ``"bold"``
* ``"heavy"``
* ``"black"``

Scale Options
~~~~~~~~~~~~~

* ``"small"`` - Small size
* ``"medium"`` - Medium size (default)
* ``"large"`` - Large size

Rendering Modes
~~~~~~~~~~~~~~~

* ``"automatic"`` - System default (default)
* ``"monochrome"`` - Single color
* ``"hierarchical"`` - Multiple opacity levels of single color
* ``"palette"`` - Multiple colors (specify with color parameters)
* ``"multicolor"`` - Built-in multicolor symbols

Color Specification
~~~~~~~~~~~~~~~~~~~

Colors can be specified as:

**Named colors (strings):**

.. code-block:: python

   "red", "blue", "green", "yellow", "orange", "purple",
   "pink", "brown", "gray", "black", "white"

**Hex colors:**

.. code-block:: python

   "#FF0000"  # Red
   "#00FF00"  # Green
   "#0000FF"  # Blue

**NSColor objects:**

.. code-block:: python

   from AppKit import NSColor
   NSColor.systemRedColor()

Examples
~~~~~~~~

**Status Icons:**

.. code-block:: python

   # Success
   success = stackit.SFSymbol("checkmark.circle.fill", color="#00FF00")

   # Warning
   warning = stackit.SFSymbol("exclamationmark.triangle.fill", color="#FFA500")

   # Error
   error = stackit.SFSymbol("xmark.circle.fill", color="#FF0000")

**Network Status:**

.. code-block:: python

   # Connected
   wifi_on = stackit.SFSymbol("wifi", point_size=16)

   # Disconnected
   wifi_off = stackit.SFSymbol("wifi.slash", point_size=16, color="#FF0000")

**System Icons:**

.. code-block:: python

   # Settings
   settings = stackit.SFSymbol("gear", point_size=20)

   # Download
   download = stackit.SFSymbol("arrow.down.circle", point_size=18)

   # Upload
   upload = stackit.SFSymbol("arrow.up.circle", point_size=18)

Finding SF Symbols
~~~~~~~~~~~~~~~~~~

To browse available SF Symbols:

1. Download Apple's SF Symbols app: https://developer.apple.com/sf-symbols/
2. Browse the complete catalog of symbols
3. Copy the symbol name to use in your app

Note: SF Symbols require macOS 11.0 or later.
