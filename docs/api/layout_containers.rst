Layout Containers
=================

block()
-------

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
