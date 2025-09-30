Quick Start
===========

Basic Application
-----------------

Here's a simple example to create a menu bar application::

    import stackit

    # Create the app
    app = stackit.StackApp("My App", "🎯")

    # Create a menu item with a custom layout
    item = stackit.StackMenuItem("Status")

    # Build the layout using hstack (horizontal stack)
    layout = item.hstack()
    layout.append(stackit.label("Server:", bold=True))
    layout.append(stackit.spacer())
    layout.append(stackit.label("Online", color="green"))

    item.set_root_stack(layout)
    app.add_item("status", item)

    # Run the app
    app.run()

Using SF Symbols
----------------

stackit has full support for macOS SF Symbols with extensive customization::

    import stackit

    app = stackit.StackApp("My App")

    # Set app icon with SF Symbol
    icon = stackit.SFSymbol.create(
        "star.fill",
        size=16,
        weight="bold",
        color="yellow"
    )
    app.set_icon(icon)

    # Add an item with SF Symbol
    item = stackit.StackMenuItem("Favorites")
    layout = item.hstack()

    star_img = stackit.image(
        stackit.SFSymbol.create("heart.fill", size=16, color="red"),
        width=16, height=16
    )
    layout.append(star_img)
    layout.append(stackit.label("My Favorites"))

    item.set_root_stack(layout)
    app.add_item("fav", item)
    app.run()

Rich UI Controls
----------------

stackit provides many built-in controls::

    import stackit

    app = stackit.StackApp("Controls Demo")
    item = stackit.StackMenuItem("Controls")

    # Create a vertical layout
    layout = item.vstack(spacing=8)

    # Add various controls
    layout.append(stackit.label("Download Progress", bold=True))
    layout.append(stackit.progress_bar(width=200, value=0.75))

    layout.append(stackit.label("Volume", bold=True))
    layout.append(stackit.slider(width=150, min_value=0, max_value=100, value=50))

    layout.append(stackit.checkbox("Enable notifications", state=True))

    layout.append(stackit.button("Click Me", target=app, action="buttonClicked:"))

    item.set_root_stack(layout)
    app.add_item("controls", item)
    app.run()

Text Input Fields
-----------------

Create menu items with various text input controls::

    import stackit

    app = stackit.StackApp("Text Input")
    item = stackit.StackMenuItem("Input")

    layout = item.vstack(spacing=4)

    # Regular text field
    layout.append(stackit.label("Name:"))
    layout.append(stackit.text_field(width=200, placeholder="Enter your name"))

    # Search field
    layout.append(stackit.label("Search:"))
    layout.append(stackit.search_field(width=200, placeholder="Search..."))

    # Secure text input (password)
    layout.append(stackit.label("Password:"))
    layout.append(stackit.secure_text_input(width=200, placeholder="Password"))

    item.set_root_stack(layout)
    app.add_item("input", item)
    app.run()
