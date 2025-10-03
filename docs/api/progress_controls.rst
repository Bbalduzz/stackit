Progress Controls
=================

progress_bar()
--------------

Create a horizontal progress bar.

.. code-block:: python

   progress = stackit.progress_bar(width=200, value=0.5, indeterminate=False)

**Parameters:**

* ``width`` (int) - Bar width in pixels (default: 200)
* ``value`` (float) - Progress value 0.0-1.0 (default: 0.0)
* ``indeterminate`` (bool) - Show indeterminate animation (default: False)

circular_progress()
-------------------

Create a circular progress indicator (spinner).

.. code-block:: python

   spinner = stackit.circular_progress(size=16, indeterminate=True)

**Parameters:**

* ``size`` (int) - Diameter in pixels (default: 32)
* ``indeterminate`` (bool) - Show indeterminate animation (default: True)
