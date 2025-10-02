StackIt
=======

.. container:: .large

   A modern, powerful framework for creating beautiful macOS menu bar applications with rich custom layouts. Build native macOS status bar apps with SwiftUI-inspired layout patterns (hstack/vstack), extensive UI controls, and full SF Symbols support.

.. container:: .buttons

   `Docs <installation.html>`_
   `GitHub <https://github.com/bbalduzz/stackit>`_

.. toctree::
   :caption: Getting Started
   :maxdepth: 2
   :hidden:

   installation
   quickstart

.. toctree::
   :caption: API Reference
   :maxdepth: 2
   :hidden:

   api/index

.. toctree::
   :caption: Examples
   :maxdepth: 2
   :hidden:

   examples

Quick Start
-----------

Install StackIt from PyPI:

.. code-block:: bash

   pip install stackitui

Create your first menu bar app:

.. code-block:: python

   import stackit

   # Create app with icon
   app = stackit.StackApp(title="Hello", icon="👋")

   # Create a menu item with custom layout
   layout = stackit.hstack([
       stackit.label("Hello, World!", bold=True)
   ])

   app.add(stackit.MenuItem(layout=layout))
   app.run()

Key Features
------------

**Rich Layouts**
   SwiftUI-inspired ``hstack``/``vstack`` for flexible, declarative layouts

**Extensive Controls**
   Labels, buttons, sliders, progress bars, text fields, checkboxes, date pickers, charts, and more

**SF Symbols**
   Full support for Apple's SF Symbols with all rendering modes (hierarchical, palette, multicolor)

**Native Performance**
   Built directly on AppKit using PyObjC, zero external dependencies

**Dynamic Updates**
   Real-time UI updates with timers and ``app.update()``

**Modern API**
   Clean, Pythonic interface with direct layout passing
