Core Module
===========

The core module provides the main classes and functions for building stackit applications.

StackApp
--------

The main application class for managing status bar applications.

.. code-block:: python

   app = stackit.StackApp(title="My App", icon="🎯")

**Methods:**

* ``add(menu_item, key=None)`` - Add a menu item (key is optional and auto-generated if not provided)
* ``remove(key)`` - Remove a menu item by key
* ``get(key)`` - Get a menu item by key
* ``add_separator()`` - Add a menu separator
* ``set_title(title)`` - Set the status bar title
* ``set_icon(icon, template=True)`` - Set the status bar icon
* ``update()`` - Force the menu to update and redraw (call after updating layouts)
* ``run()`` - Start the application event loop (automatically adds Quit button)

MenuItem
--------

Menu items can be either simple (title-based) or custom (layout-based).

**Simple Menu Items:**

.. code-block:: python

   # Text-based menu item with callback and keyboard shortcut
   item = stackit.MenuItem(
       title="Preferences",
       callback=open_prefs,
       key_equivalent=","  # ⌘,
   )
   app.add(item)

**Custom Layout Menu Items:**

.. code-block:: python

   # Pass layout directly in constructor
   item = stackit.MenuItem(layout=stackit.hstack([
       stackit.label("Hello"),
       stackit.spacer(),
       stackit.label("World")
   ]))

   # Or create and set layout later
   item = stackit.MenuItem()
   item.set_layout(my_layout)

**Parameters:**

* ``title`` - Optional title text for simple menu items (mutually exclusive with layout)
* ``layout`` - Optional layout to display (StackView instance, mutually exclusive with title)
* ``callback`` - Optional callback function for menu item clicks
* ``key_equivalent`` - Optional keyboard shortcut (e.g., "q" for ⌘Q, "," for ⌘,)

**Methods:**

* ``set_layout(stack_view)`` - Set or update the layout for the menu item
* ``set_callback(callback)`` - Set or update the callback function
* ``menuitem()`` - Get the underlying NSMenuItem

**Note:** Use ``title`` for simple text menu items, or ``layout`` for rich custom layouts. Don't use both together.

Layout Functions
----------------

Standalone functions for creating layouts.

hstack()
~~~~~~~~

Create a horizontal stack view.

.. code-block:: python

   layout = stackit.hstack([
       stackit.label("Status:"),
       stackit.spacer(),
       stackit.label("Active", color="green")
   ], spacing=8.0)

**Parameters:**

* ``controls`` - Optional list of controls to add
* ``alignment`` - Optional alignment (NSLayoutAttribute constant)
* ``spacing`` - Spacing between controls in points (default: 8.0)

**Returns:** StackView configured for horizontal layout

vstack()
~~~~~~~~

Create a vertical stack view.

.. code-block:: python

   layout = stackit.vstack([
       stackit.label("Title", bold=True),
       stackit.progress_bar(value=0.75),
       stackit.button("Submit", callback=my_callback)
   ], spacing=12.0)

**Parameters:**

* ``controls`` - Optional list of controls to add
* ``alignment`` - Optional alignment (NSLayoutAttribute constant)
* ``spacing`` - Spacing between controls in points (default: 8.0)

**Returns:** StackView configured for vertical layout

StackView
---------

Container for arranging UI elements in horizontal or vertical layouts.
Created by ``hstack()`` and ``vstack()`` functions.

.. code-block:: python

   # Create stacks
   hstack = stackit.hstack(spacing=8)
   vstack = stackit.vstack(spacing=4)

   # Dynamically add controls
   vstack.append(stackit.label("New item"))
   vstack.extend([label1, label2, label3])

**List-like Methods:**

* ``append(view)`` - Add a view to the end
* ``extend(views)`` - Add multiple views
* ``insert(index, view)`` - Insert view at index
* ``remove(view)`` - Remove a view
* ``clear()`` - Remove all views

**Alignment Constants:**

* ``NSLayoutAttributeLeading`` - Left alignment (horizontal) or top (vertical)
* ``NSLayoutAttributeCenterX`` - Center horizontally
* ``NSLayoutAttributeCenterY`` - Center vertically
* ``NSLayoutAttributeTrailing`` - Right alignment (horizontal) or bottom (vertical)
