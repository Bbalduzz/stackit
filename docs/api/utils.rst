Utils Module
============

The utils module provides utility functions for common tasks.

User Interaction
----------------

alert()
~~~~~~~

Display an alert dialog.

.. code-block:: python

   # Simple alert
   stackit.alert("Title", "Message text")

   # Alert with custom buttons
   result = stackit.alert(
       "Confirm Action",
       "Are you sure you want to continue?",
       ok="Yes",
       cancel="No"
   )
   if result == 1:  # OK button clicked
       print("User confirmed")

   # Alert with custom icon
   stackit.alert(
       "Error",
       "An error occurred",
       icon_path="/path/to/icon.png"
   )

**Parameters:**

* ``title`` (str) - Alert title
* ``message`` (str) - Alert message
* ``ok`` (str) - OK button text (default: "OK")
* ``cancel`` (str) - Cancel button text (default: None for no cancel button)
* ``icon_path`` (str) - Path to custom icon image (optional)

**Returns:**

* ``1`` if OK clicked
* ``0`` if Cancel clicked

notification()
~~~~~~~~~~~~~~

Display a system notification.

.. code-block:: python

   # Basic notification
   stackit.notification("Title", "Subtitle", "Message body")

   # Silent notification
   stackit.notification(
       "Background Task",
       subtitle="Complete",
       message="Your task has finished",
       sound=False
   )

**Parameters:**

* ``title`` (str) - Notification title
* ``subtitle`` (str) - Notification subtitle (optional)
* ``message`` (str) - Notification body text
* ``sound`` (bool) - Play notification sound (default: True)

File Operations
---------------

choose_directory()
~~~~~~~~~~~~~~~~~~

Open a directory picker dialog.

.. code-block:: python

   path = stackit.choose_directory(
       title="Select Folder",
       default_path="/Users/username/Documents"
   )
   if path:
       print(f"Selected: {path}")

**Parameters:**

* ``title`` (str) - Dialog title (optional)
* ``default_path`` (str) - Initial directory path (optional)

**Returns:**

* Selected directory path as string, or ``None`` if cancelled

Preferences
-----------

save_preferences()
~~~~~~~~~~~~~~~~~~

Save application preferences.

.. code-block:: python

   stackit.save_preferences("MyApp", {
       "theme": "dark",
       "notifications": True,
       "refresh_interval": 60
   })

**Parameters:**

* ``app_name`` (str) - Application identifier
* ``preferences`` (dict) - Dictionary of preferences to save

load_preferences()
~~~~~~~~~~~~~~~~~~

Load application preferences.

.. code-block:: python

   prefs = stackit.load_preferences("MyApp", defaults={
       "theme": "light",
       "notifications": False,
       "refresh_interval": 30
   })

   print(prefs["theme"])  # Returns saved value or default

**Parameters:**

* ``app_name`` (str) - Application identifier
* ``defaults`` (dict) - Default values if no preferences saved (optional)

**Returns:**

* Dictionary of preferences

Timers
------

All timer functions use ``NSRunLoopCommonModes`` to ensure timers continue firing even when menus are open. This is essential for dynamic menu updates.

timer()
~~~~~~~

Create a repeating or one-shot timer.

.. code-block:: python

   def update_status(timer):
       print("Timer fired!")

   # Repeating timer (every 5 seconds)
   timer = stackit.timer(5.0, update_status, repeats=True)

   # One-shot timer
   timer = stackit.timer(10.0, update_status, repeats=False)

**Parameters:**

* ``interval`` (float) - Time interval in seconds
* ``callback`` (callable) - Function to call when timer fires
* ``repeats`` (bool) - Whether timer should repeat (default: True)

**Returns:**

* NSTimer object (keep reference to prevent garbage collection)

after()
~~~~~~~

Execute a function after a delay (convenience wrapper for one-shot timer).

.. code-block:: python

   def delayed_action(timer):
       print("Executed after 3 seconds")

   stackit.after(3.0, delayed_action)

**Parameters:**

* ``delay`` (float) - Delay in seconds
* ``callback`` (callable) - Function to execute

every()
~~~~~~~

Execute a function repeatedly (convenience wrapper for repeating timer).

.. code-block:: python

   def periodic_update(timer):
       print("Updating...")
       # Update UI
       app.update()  # Force menu to redraw

   timer = stackit.every(10.0, periodic_update)

**Parameters:**

* ``interval`` (float) - Interval in seconds
* ``callback`` (callable) - Function to execute

**Returns:**

* NSTimer object

**Note:** When updating menu layouts in timer callbacks, call ``app.update()`` to force the menu to redraw.

Application Control
-------------------

quit_application()
~~~~~~~~~~~~~~~~~~

Quit the application.

.. code-block:: python

   stackit.quit_application()

open_url()
~~~~~~~~~~

Open a URL in the default browser (if implemented).

.. code-block:: python

   stackit.open_url("https://example.com")

**Parameters:**

* ``url`` (str) - URL to open
