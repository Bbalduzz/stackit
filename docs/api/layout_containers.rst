Layout Containers
=================

window()
--------

Create a standalone NSWindow that can contain StacKit controls.

.. code-block:: python

   # Create a basic window
   win = stackit.window(title="Settings", size=(400, 300))

   # Create layout with controls
   content = stackit.vstack([
       stackit.label("Application Settings", bold=True, font_size=16),
       stackit.separator(),
       stackit.text_field(placeholder="Enter value"),
       stackit.button("Save", callback=save_handler),
   ], spacing=12.0)

   # Add layout to window
   stackit.window_layout(win, content, padding=(20, 20, 20, 20))

   # Show window
   win.makeKeyAndOrderFront_(None)

   # Customize window style
   custom_win = stackit.window(
       title="Preferences",
       size=(500, 400),
       resizable=True,
       closable=True,
       miniaturizable=True,
       titled=True
   )

**Parameters:**

* ``title`` (str, optional) - Window title
* ``size`` (tuple) - Window dimensions as (width, height) in points (default: (600, 400))
* ``resizable`` (bool) - Whether window can be resized (default: True)
* ``closable`` (bool) - Whether window has close button (default: True)
* ``miniaturizable`` (bool) - Whether window can be minimized (default: True)
* ``titled`` (bool) - Whether window has title bar (default: True)

**Returns:** NSWindow instance

**Note:** Use with ``window_layout()`` to add StacKit layouts to the window.

window_layout()
---------------

Add a layout (stack or single control) to a window with proper constraints.

.. code-block:: python

   # Create window and layout
   win = stackit.window(title="My App", size=(400, 300))

   content = stackit.vstack([
       stackit.label("Username:", bold=True),
       stackit.text_field(placeholder="Enter username"),
       stackit.button("Submit", callback=submit_handler)
   ], spacing=12.0)

   # Add layout with custom padding
   stackit.window_layout(win, content, padding=(20, 20, 20, 20))

   # Show window
   win.makeKeyAndOrderFront_(None)

   # Different padding for each edge
   stackit.window_layout(
       win,
       content,
       padding=(30, 40, 30, 40)  # (top, leading, bottom, trailing)
   )

**Parameters:**

* ``window`` (NSWindow) - The window to add the layout to
* ``layout`` (NSView) - A StackView (from hstack/vstack) or any NSView control
* ``padding`` (tuple) - Edge insets as (top, leading, bottom, trailing) in points (default: (20, 20, 20, 20))

**Returns:** The layout view that was added

**Note:** This helper handles all Auto Layout constraints automatically. All callbacks in windows (buttons, etc.) receive a ``sender`` parameter.

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
