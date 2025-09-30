Core Module
===========

The core module provides the main classes for building stackit applications.

StackApp
--------

The main application class for managing status bar applications.

.. code-block:: python

   app = stackit.StackApp(title="My App", icon="🎯")

**Methods:**

* ``add_item(key, stack_menu_item)`` - Add a menu item
* ``remove_item(key)`` - Remove a menu item by key
* ``get_item(key)`` - Get a menu item by key
* ``add_separator()`` - Add a menu separator
* ``set_title(title)`` - Set the status bar title
* ``set_icon(icon)`` - Set the status bar icon
* ``run()`` - Start the application event loop

StackMenuItem
-------------

Rich menu items with custom layouts using hstack/vstack.

.. code-block:: python

   item = stackit.StackMenuItem(title="My Item", callback=my_callback)

**Layout Methods:**

* ``hstack(alignment=None, spacing=8)`` - Create horizontal stack
* ``vstack(alignment=None, spacing=8)`` - Create vertical stack
* ``set_root_stack(stack)`` - Set the root layout for the menu item

**Control Creation Methods:**

* ``label(text, font_size=13, bold=False, color=None)`` - Create a label
* ``button(title, target=None, action=None)`` - Create a button
* ``image_view(image_path, width=24, height=24)`` - Create an image view
* ``spacer(priority=250)`` - Create a flexible spacer

StackView
---------

Container for arranging UI elements in horizontal or vertical layouts.

.. code-block:: python

   # Create stacks
   hstack = item.hstack(spacing=8)
   vstack = item.vstack(spacing=4)

**List-like Methods:**

* ``append(view)`` - Add a view to the end
* ``extend(views)`` - Add multiple views
* ``insert(index, view)`` - Insert view at index
* ``remove(view)`` - Remove a view
* ``clear()`` - Remove all views
* ``__len__()`` - Get number of views
* ``__getitem__(index)`` - Get view by index

**Alignment Constants:**

* ``NSLayoutAttributeLeading`` - Left alignment (horizontal) or top (vertical)
* ``NSLayoutAttributeCenterX`` - Center horizontally
* ``NSLayoutAttributeCenterY`` - Center vertically
* ``NSLayoutAttributeTrailing`` - Right alignment (horizontal) or bottom (vertical)
