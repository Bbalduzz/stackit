Image Controls
==============

image()
-------

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
