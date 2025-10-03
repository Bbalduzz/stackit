Media Controls
==============

video()
-------

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
----------

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
----------

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
