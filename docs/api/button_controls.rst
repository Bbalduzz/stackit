Button Controls
===============

button()
--------

Create a clickable button.

.. code-block:: python

   btn = stackit.button("Click Me", target=self, action="buttonClicked:")

**Parameters:**

* ``title`` (str) - Button text
* ``target`` (object) - Target object for action (optional)
* ``action`` (str) - Selector string for action (optional)

checkbox()
----------

Create a checkbox control.

.. code-block:: python

   checkbox = stackit.checkbox("Enable feature", state=True)

**Parameters:**

* ``title`` (str) - Checkbox label
* ``state`` (bool) - Initial checked state (default: False)

radio_button()
--------------

Create a single radio button.

.. code-block:: python

   radio = stackit.radio_button("Option 1", state=False)

**Note:** For proper mutually exclusive radio button groups, use ``radio_group()`` instead.

radio_group()
-------------

Create a group of mutually exclusive radio buttons.

.. code-block:: python

   # Simple string labels (default)
   def handle_selection(sender):
       print(f"Selected: {sender.title()}")

   group = stackit.radio_group(
       options=["Small", "Medium", "Large"],
       selected=1,  # Medium is initially selected
       callback=handle_selection
   )

   # Horizontal radio group
   color_group = stackit.radio_group(
       options=["Red", "Green", "Blue"],
       selected=0,
       orientation="horizontal",
       spacing=12.0
   )

   # Pre-configured radio buttons for more control
   custom_group = stackit.radio_group(
       options=[
           stackit.radio_button("Option A"),
           stackit.radio_button("Option B"),
           stackit.radio_button("Option C")
       ],
       selected=0,
       callback=handle_selection
   )

**Parameters:**

* ``options`` (list[str] or list[NSButton]) - List of radio button labels (strings) or pre-configured radio buttons
* ``selected`` (int) - Index of initially selected option (default: 0)
* ``orientation`` (str) - Layout orientation: "vertical" or "horizontal" (default: "vertical")
* ``spacing`` (float) - Spacing between buttons in points (default: 8.0)
* ``callback`` (callable) - Function called when selection changes, receives the selected NSButton
* ``**kwargs`` - Additional attributes (only applied when options are strings)

**Returns:** StackView containing the radio button group with mutual exclusivity
