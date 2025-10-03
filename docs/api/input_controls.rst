Input Controls
==============

text_field()
------------

Create a text input field.

.. code-block:: python

   field = stackit.text_field(width=200, placeholder="Enter text", font_size=13)

**Parameters:**

* ``width`` (int) - Field width in pixels (default: 200)
* ``placeholder`` (str) - Placeholder text (optional)
* ``font_size`` (int) - Font size (default: 13)

secure_text_input()
-------------------

Create a secure text input field (for passwords).

.. code-block:: python

   password = stackit.secure_text_input(width=200, placeholder="Password")

search_field()
--------------

Create a search input field with search icon.

.. code-block:: python

   search = stackit.search_field(width=200, placeholder="Search...")
