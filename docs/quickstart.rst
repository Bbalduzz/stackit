Quick Start
===========

Basic Application
-----------------

Here's a simple example to create a menu bar application::

    import stackit

    # Create the app
    app = stackit.StackApp("My App", "🎯")

    # Create a menu item with layout directly
    item = stackit.MenuItem(layout=stackit.hstack([
        stackit.label("Server:", bold=True),
        stackit.spacer(),
        stackit.label("Online", color="green")
    ]))

    app.add(item)  # No key needed
    app.run()

Simple Menu Items
-----------------

For simple text-based menu items (like Preferences, About, etc.)::

    import stackit

    app = stackit.StackApp("My App")

    def open_preferences(sender):
        print("Opening preferences...")

    def show_about(sender):
        stackit.alert("About", "My App v1.0")

    # Simple menu items with keyboard shortcuts
    prefs = stackit.MenuItem(
        title="Preferences...",
        callback=open_preferences,
        key_equivalent=","  # ⌘,
    )
    app.add(prefs)

    about = stackit.MenuItem(
        title="About",
        callback=show_about
    )
    app.add(about)

    app.run()

Building Layouts
----------------

You can build layouts before passing them to MenuItem::

    import stackit

    app = stackit.StackApp("My App")

    # Build the layout first
    layout = stackit.vstack([
        stackit.hstack([
            stackit.label("Status:", bold=True),
            stackit.spacer(),
            stackit.label("Active", color="green")
        ]),
        stackit.progress_bar(value=0.75),
        stackit.button("Refresh", callback=lambda s: print("Refresh!"))
    ], spacing=12.0)

    # Pass layout to MenuItem
    item = stackit.MenuItem(layout=layout)
    app.add(item)
    app.run()

Using SF Symbols
----------------

stackit has full support for macOS SF Symbols with extensive customization::

    import stackit

    app = stackit.StackApp("My App")

    # Set app icon with SF Symbol
    icon = stackit.SFSymbol(
        "star.fill",
        point_size=16,
        weight="bold",
        color="yellow"
    )
    app.set_icon(icon)

    # Add an item with SF Symbol
    layout = stackit.hstack([
        stackit.image(
            stackit.SFSymbol("heart.fill", point_size=16, color="red"),
            width=16, height=16
        ),
        stackit.label("My Favorites")
    ])

    item = stackit.MenuItem(layout=layout)
    app.add(item)
    app.run()

SF Symbol Rendering Modes
--------------------------

SF Symbols support different rendering modes for enhanced visual effects::

    import stackit

    app = stackit.StackApp("Symbols")

    # Monochrome: Single solid color
    mono_symbol = stackit.SFSymbol(
        "heart.fill",
        rendering="monochrome",
        color="#FF0000",
        point_size=20
    )

    # Hierarchical: Base color with derived opacity levels for depth
    hierarchical_symbol = stackit.SFSymbol(
        "cloud.sun.fill",
        rendering="hierarchical",
        color="#0000FF",
        point_size=20
    )

    # Palette: Multiple explicit colors for different symbol layers
    palette_symbol = stackit.SFSymbol(
        "flag.fill",
        rendering="palette",
        palette_colors=["#FF0000", "#00FF00", "#0000FF"],
        point_size=20
    )

    # Multicolor: Uses the symbol's built-in colors
    multicolor_symbol = stackit.SFSymbol(
        "rainbow",
        rendering="multicolor",
        point_size=20
    )

**Available Rendering Modes:**

* ``monochrome`` - Single color for entire symbol
* ``hierarchical`` - Base color with automatic opacity variations for depth
* ``palette`` - Explicit colors for each layer (use ``palette_colors`` parameter)
* ``multicolor`` - Symbol's built-in color scheme
* ``automatic`` - System decides best rendering (default)

Blocks with Borders
-------------------

Add visual structure with bordered containers (like the Network stats example)::

    import stackit

    app = stackit.StackApp("Stats")

    # Create content
    network_content = stackit.vstack([
        stackit.label("Network", bold=True, font_size=14),
        stackit.hstack([
            stackit.vstack([
                stackit.label("Out", font_size=10, color="gray"),
                stackit.label("1 KB/s", font_size=12)
            ]),
            stackit.spacer(),
            stackit.vstack([
                stackit.label("In", font_size=10, color="gray"),
                stackit.label("0 KB/s", font_size=12)
            ])
        ])
    ])

    # Wrap in a block with border and background
    network_block = stackit.block(network_content, radius=8.0, padding=12.0)

    item = stackit.MenuItem(layout=network_block)
    app.add(item)
    app.run()

Images with Rounded Corners
----------------------------

Add visual polish with rounded corners on images::

    import stackit

    app = stackit.StackApp("Gallery")

    layout = stackit.vstack([
        # Slightly rounded corners
        stackit.image(
            "https://picsum.photos/100/100",
            width=100,
            height=100,
            border_radius=8.0
        ),

        # Circular profile picture
        stackit.image(
            "https://picsum.photos/50/50",
            width=50,
            height=50,
            border_radius=25.0  # Half of width/height = circle
        ),
    ])

    item = stackit.MenuItem(layout=layout)
    app.add(item)
    app.run()

Rich UI Controls
----------------

stackit provides many built-in controls::

    import stackit

    app = stackit.StackApp("Controls Demo")

    # Create layout with various controls
    layout = stackit.vstack([
        stackit.label("Download Progress", bold=True),
        stackit.progress_bar(value=0.75),

        stackit.label("Volume", bold=True),
        stackit.slider(width=150, min_value=0, max_value=100, value=50),

        stackit.checkbox("Enable notifications", checked=True),

        stackit.button("Click Me", callback=lambda s: print("Clicked!"))
    ], spacing=8)

    item = stackit.MenuItem(layout=layout)
    app.add(item)
    app.run()

Text Input Fields
-----------------

Create menu items with various text input controls::

    import stackit

    app = stackit.StackApp("Text Input")

    layout = stackit.vstack([
        stackit.label("Name:"),
        stackit.text_field(size=(200, 25), placeholder="Enter your name"),

        stackit.label("Search:"),
        stackit.search_field(size=(200, 25), placeholder="Search..."),

        stackit.label("Password:"),
        stackit.secure_text_input(width=200, placeholder="Password")
    ], spacing=4)

    item = stackit.MenuItem(layout=layout)
    app.add(item)
    app.run()

Status Bar Updates
------------------

Update the status bar icon and title at runtime::

    import stackit

    # Create app with both icon and title
    app = stackit.StackApp(
        title="Idle",
        icon=stackit.SFSymbol("circle", color="#999999")
    )

    def update_to_working():
        # Both icon and title can be updated
        app.set_icon(stackit.SFSymbol("circle.fill", color="#FF9500"))
        app.set_title("Working")

    def update_to_done():
        app.set_icon(stackit.SFSymbol("checkmark.circle.fill", color="#34C759"))
        app.set_title("Done")

    # Add buttons to trigger updates
    app.add(stackit.MenuItem(title="Start Working", callback=lambda s: update_to_working()))
    app.add(stackit.MenuItem(title="Mark Done", callback=lambda s: update_to_done()))
    app.run()

**Note:** Both icon and title are displayed simultaneously in the status bar.

Line Charts
-----------

Create smooth line charts with spline interpolation using SpriteKit::

    import stackit

    app = stackit.StackApp("System Monitor")

    # Sample CPU usage data
    cpu_data = [10, 15, 8, 20, 18, 25, 22, 26, 24, 26]

    layout = stackit.hstack([
        stackit.label("CPU:", bold=True),
        stackit.spacer(),
        stackit.label("26%"),
        stackit.line_chart(
            points=cpu_data,
            dimensions=(60, 20),
            max_value=100.0,
            line_width=1.0,
            fill=True
        )
    ])

    item = stackit.MenuItem(layout=layout)
    app.add(item)
    app.run()

**Note:** The line_chart control uses SpriteKit's SKKeyframeSequence for smooth spline interpolation, creating fluid curves like the original Swift implementation.

Dynamic Menu Updates
--------------------

Update menu item layouts dynamically::

    import stackit
    import time

    app = stackit.StackApp("Timer")

    # Create MenuItem without layout
    item = stackit.MenuItem()
    app.add(item, key="timer")  # Optional key for later reference

    start_time = time.time()

    def update_timer(timer):
        elapsed = int(time.time() - start_time)
        minutes, seconds = divmod(elapsed, 60)

        # Update layout dynamically
        new_layout = stackit.hstack([
            stackit.label("Time:", bold=True),
            stackit.spacer(),
            stackit.label(f"{minutes:02d}:{seconds:02d}")
        ])
        item.set_layout(new_layout)

        # Force menu to redraw (needed for updates while menu is open)
        app.update()

    # Update every second (timer continues even when menu is open)
    stackit.every(1.0, update_timer)
    update_timer(None)  # Initial update
    app.run()
