Selection Controls
==================

combobox()
----------

Create a combo box (dropdown menu).

.. code-block:: python

   combo = stackit.combobox(
       items=["Option 1", "Option 2", "Option 3"],
       width=200,
       editable=False
   )

**Parameters:**

* ``items`` (list) - List of string items
* ``width`` (int) - Width in pixels (default: 200)
* ``editable`` (bool) - Allow text editing (default: False)
