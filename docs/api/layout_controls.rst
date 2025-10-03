Layout Controls
===============

spacer()
--------

Create a flexible spacer that expands to fill available space.

.. code-block:: python

   spacer = stackit.spacer(priority=250)

**Parameters:**

* ``priority`` (int) - Hugging priority (default: 250). Lower = more expansion.

separator()
-----------

Create a horizontal separator line.

.. code-block:: python

   sep = stackit.separator(width=200)

**Parameters:**

* ``width`` (int) - Separator width in pixels (default: 200)
