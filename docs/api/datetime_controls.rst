Date and Time Controls
======================

date_picker()
-------------

Create a date picker control.

.. code-block:: python

   picker = stackit.date_picker(
       date=datetime.now(),
       date_only=True,
       width=200
   )

**Parameters:**

* ``date`` (datetime) - Initial date (default: now)
* ``date_only`` (bool) - Show only date, not time (default: True)
* ``width`` (int) - Width in pixels (default: 200)

time_picker()
-------------

Create a time picker control.

.. code-block:: python

   picker = stackit.time_picker(
       time=datetime.now(),
       width=150
   )

**Parameters:**

* ``time`` (datetime) - Initial time (default: now)
* ``width`` (int) - Width in pixels (default: 150)
