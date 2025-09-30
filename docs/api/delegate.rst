Delegate Module
===============

The delegate module provides application lifecycle management.

StackAppDelegate
----------------

The StackAppDelegate class handles application lifecycle events and system integration.

Overview
~~~~~~~~

The delegate is automatically created and configured by StackApp. You typically don't need to interact with it directly, but understanding its role can help with advanced usage.

Lifecycle Events
~~~~~~~~~~~~~~~~

The delegate handles these key application events:

**Application Launch:**

* ``applicationDidFinishLaunching_`` - Called when app finishes launching
* Initializes status bar
* Sets up workspace notifications

**Sleep/Wake Events:**

* ``workspaceWillSleep_`` - Called before system sleeps
* ``workspaceDidWake_`` - Called after system wakes

**Application Termination:**

* ``applicationWillTerminate_`` - Called before app quits
* Clean up resources

Callback Registry
~~~~~~~~~~~~~~~~~

The delegate maintains a callback registry for menu item actions:

.. code-block:: python

   # Internal usage - handled automatically by StackMenuItem
   StackAppDelegate._callback_registry[menuitem] = (stack_item, callback)

When a menu item is clicked or an action is triggered, the delegate:

1. Looks up the callback in the registry
2. Executes the callback with proper error handling
3. Logs any exceptions

Custom Delegate Methods
~~~~~~~~~~~~~~~~~~~~~~~

For advanced usage, you can extend the delegate behavior:

.. code-block:: python

   import stackit
   from stackit.delegate import StackAppDelegate

   class MyCustomDelegate(StackAppDelegate):
       def applicationDidFinishLaunching_(self, notification):
           # Call parent implementation
           super().applicationDidFinishLaunching_(notification)

           # Add custom initialization
           print("Custom app initialization")

       def workspaceDidWake_(self, notification):
           super().workspaceDidWake_(notification)
           print("System woke up - refresh data")

   # Use custom delegate
   app = stackit.StackApp("My App")
   # Note: Setting custom delegate requires accessing internal APIs

Error Handling
~~~~~~~~~~~~~~

The delegate provides robust error handling for callbacks:

.. code-block:: python

   def my_callback(sender):
       raise Exception("Something went wrong")

   # Exception will be caught, logged, and won't crash the app
   item = stackit.StackMenuItem("Test", callback=my_callback)

Errors are logged using NSLog and include:

* Error message
* Stack trace
* Context information

Workspace Notifications
~~~~~~~~~~~~~~~~~~~~~~~

The delegate automatically observes these workspace notifications:

* ``NSWorkspaceWillSleepNotification`` - System going to sleep
* ``NSWorkspaceDidWakeNotification`` - System woke from sleep
* ``NSWorkspaceDidActivateApplicationNotification`` - App activated
* ``NSWorkspaceDidDeactivateApplicationNotification`` - App deactivated

These enable your app to respond to system events automatically.

Best Practices
~~~~~~~~~~~~~~

1. **Don't create delegates manually** - Let StackApp handle it
2. **Use callbacks for actions** - Register callbacks through StackMenuItem
3. **Handle errors in callbacks** - Don't rely on delegate error handling
4. **Keep callbacks lightweight** - Avoid long-running operations
5. **Use timers for periodic updates** - Don't block the main thread

Example: Responding to System Events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import stackit

   class MyApp:
       def __init__(self):
           self.app = stackit.StackApp("System Monitor")
           self.setup_ui()

       def setup_ui(self):
           # Create status item
           item = stackit.StackMenuItem("Status")
           layout = item.hstack()
           layout.append(stackit.label("Ready"))
           item.set_root_stack(layout)
           self.app.add_item("status", item)

       def run(self):
           # Delegate handles lifecycle automatically
           self.app.run()

   MyApp().run()

The delegate ensures your app integrates properly with macOS and handles system events gracefully.
