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
   icon = stackit.SFSymbol.create("star.fill")

   # With size and weight
   icon = stackit.SFSymbol.create("star.fill", size=20, weight="bold")

   # With color
   icon = stackit.SFSymbol.create("heart.fill", size=16, color="red")

   # With hierarchical rendering
   icon = stackit.SFSymbol.create(
       "gear",
       size=24,
       weight="semibold",
       rendering_mode="hierarchical"
   )

   # Multicolor symbols
   icon = stackit.SFSymbol.create(
       "heart.circle.fill",
       size=32,
       rendering_mode="multicolor"
   )

create()
~~~~~~~~

Create an SF Symbol image.

**Parameters:**

* ``symbol_name`` (str) - SF Symbol name (e.g., "star.fill", "heart", "gear")
* ``size`` (int) - Point size (default: 13)
* ``weight`` (str) - Font weight (default: "regular")
* ``scale`` (str) - Symbol scale: "small", "medium", "large" (default: "medium")
* ``rendering_mode`` (str) - Rendering mode (default: "automatic")
* ``color`` (str or NSColor) - Primary color (optional)
* ``secondary_color`` (str or NSColor) - Secondary color for palette mode (optional)
* ``tertiary_color`` (str or NSColor) - Tertiary color for palette mode (optional)

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
   success = stackit.SFSymbol.create("checkmark.circle.fill", color="green")

   # Warning
   warning = stackit.SFSymbol.create("exclamationmark.triangle.fill", color="orange")

   # Error
   error = stackit.SFSymbol.create("xmark.circle.fill", color="red")

**Network Status:**

.. code-block:: python

   # Connected
   wifi_on = stackit.SFSymbol.create("wifi", size=16)

   # Disconnected
   wifi_off = stackit.SFSymbol.create("wifi.slash", size=16, color="red")

**System Icons:**

.. code-block:: python

   # Settings
   settings = stackit.SFSymbol.create("gear", size=20)

   # Download
   download = stackit.SFSymbol.create("arrow.down.circle", size=18)

   # Upload
   upload = stackit.SFSymbol.create("arrow.up.circle", size=18)

Finding SF Symbols
~~~~~~~~~~~~~~~~~~

To browse available SF Symbols:

1. Download Apple's SF Symbols app: https://developer.apple.com/sf-symbols/
2. Browse the complete catalog of symbols
3. Copy the symbol name to use in your app

Note: SF Symbols require macOS 11.0 or later.
