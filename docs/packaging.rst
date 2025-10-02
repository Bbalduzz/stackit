Packaging Applications
======================

This guide shows how to package your StackIt applications as standalone macOS ``.app`` bundles using py2app.

Prerequisites
-------------

1. **Install py2app:**

   .. code-block:: bash

      pip install py2app

2. **Ensure StacKit is installed:**

   .. code-block:: bash

      # Development mode (recommended)
      cd /path/to/stackit
      pip install -e .

      # Or from PyPI
      pip install stackitui

Creating a Setup File
---------------------

Create a ``setup.py`` file for your application:

.. code-block:: python

   from setuptools import setup
   import sys
   import os

   # Add parent directory to path if stackit is local
   sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

   APP = ['your_app.py']
   DATA_FILES = []
   OPTIONS = {
       'argv_emulation': False,
       'plist': {
           'CFBundleName': 'YourApp',
           'CFBundleDisplayName': 'Your App Display Name',
           'CFBundleIdentifier': 'com.yourcompany.yourapp',
           'CFBundleVersion': '1.0.0',
           'CFBundleShortVersionString': '1.0',
           'LSUIElement': True,  # Menu bar app (no Dock icon)
           'NSHighResolutionCapable': True,
           'NSRequiresAquaSystemAppearance': False,  # Support dark mode
       },
       'packages': [
           'stackit',
           'AppKit',
           'Foundation',
           'objc',
       ],
       'includes': [
           'stackit.core',
           'stackit.controls',
           'stackit.sfsymbol',
           'stackit.utils',
           'stackit.delegate',
       ],
       'excludes': [
           'tkinter',
           'matplotlib',
           'numpy',
           'scipy',
           'pandas',
           'pytest',
           'IPython',
       ],
       'strip': True,
       'optimize': 2,
   }

   setup(
       name='YourApp',
       app=APP,
       data_files=DATA_FILES,
       options={'py2app': OPTIONS},
       setup_requires=['py2app'],
   )

Building the Application
-------------------------

Development Build (Alias Mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For development and testing, use alias mode (``-A``). This creates a lightweight build that links to your source files:

.. code-block:: bash

   python setup.py py2app -A

**Advantages:**

- Builds in seconds
- Changes to source code are immediately reflected
- Perfect for iteration and testing
- Much smaller app size

**Limitations:**

- Requires Python to be installed on the system
- Not suitable for distribution

Standalone Build
~~~~~~~~~~~~~~~~

For distribution, create a full standalone build:

.. code-block:: bash

   python setup.py py2app

**Advantages:**

- Bundles Python and all dependencies
- Can be distributed to users without Python
- Self-contained application

**Limitations:**

- Takes longer to build (minutes)
- Larger app size (50-100 MB)
- May have issues with editable installs

.. note::

   If you encounter "No module named 'stackit'" errors during standalone builds, use alias mode (``-A``) instead. The standalone build can have issues with editable installs.

Testing the Application
-----------------------

After building, test your application:

.. code-block:: bash

   open dist/YourApp.app

Check the Console.app for any runtime errors or warnings.

Customization
-------------

Adding an Icon
~~~~~~~~~~~~~~

Create or download an ``.icns`` file and add it to your setup:

.. code-block:: python

   OPTIONS = {
       'iconfile': 'path/to/icon.icns',
       # ... other options
   }

Bundle Information
~~~~~~~~~~~~~~~~~~

Customize the app's bundle information in the plist:

.. code-block:: python

   'plist': {
       'CFBundleName': 'MyApp',                    # Internal name
       'CFBundleDisplayName': 'My Application',    # Display name
       'CFBundleIdentifier': 'com.mycompany.myapp',
       'CFBundleVersion': '1.0.0',
       'CFBundleShortVersionString': '1.0',
       'LSMinimumSystemVersion': '10.15.0',        # Minimum macOS version
   }

Permissions
~~~~~~~~~~~

If your app needs special permissions (like Full Disk Access), add usage descriptions:

.. code-block:: python

   'plist': {
       # ... other settings
       'NSAppleEventsUsageDescription': 'Your app needs to access system events.',
       'NSSystemAdministrationUsageDescription': 'Your app needs Full Disk Access.',
   }

Reducing App Size
~~~~~~~~~~~~~~~~~

Add unused packages to the excludes list:

.. code-block:: python

   'excludes': [
       'tkinter',
       'matplotlib',
       'numpy',
       'scipy',
       'pandas',
       'pytest',
       'IPython',
       # Add more as needed
   ]

Distribution
------------

Option 1: ZIP Archive
~~~~~~~~~~~~~~~~~~~~~

Create a ZIP file for easy distribution:

.. code-block:: bash

   cd dist
   zip -r YourApp.zip YourApp.app

Users can download, unzip, and drag to ``/Applications``.

Option 2: DMG Installer
~~~~~~~~~~~~~~~~~~~~~~~~

Create a professional disk image installer:

.. code-block:: bash

   # Install create-dmg
   brew install create-dmg

   # Create DMG
   create-dmg \
     --volname "YourApp Installer" \
     --window-pos 200 120 \
     --window-size 600 400 \
     --icon-size 100 \
     --icon "YourApp.app" 175 120 \
     --hide-extension "YourApp.app" \
     --app-drop-link 425 120 \
     "YourApp.dmg" \
     "dist/"

Option 3: Code Signing
~~~~~~~~~~~~~~~~~~~~~~~

To avoid "unidentified developer" warnings (requires Apple Developer account):

.. code-block:: bash

   # Sign the app
   codesign --deep --force --sign "Developer ID Application: Your Name" dist/YourApp.app

   # Verify signature
   codesign --verify --verbose dist/YourApp.app

   # Notarize with Apple
   xcrun notarytool submit YourApp.zip --apple-id your@email.com --wait

Troubleshooting
---------------

ImportError: No module named 'stackit'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:**

- Ensure stackit is installed: ``pip install -e /path/to/stackit``
- Use alias mode: ``python setup.py py2app -A``

App won't launch
~~~~~~~~~~~~~~~~

**Solution:**

- Open Console.app and filter for your app name to see error messages
- Ensure you used alias mode: ``python setup.py py2app -A``
- Check that all required modules are in the ``packages`` list

Missing modules at runtime
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:**

Add the missing module to the ``packages`` list in your setup file:

.. code-block:: python

   'packages': [
       'stackit',
       'your_missing_module',
       # ...
   ]

App too large
~~~~~~~~~~~~~

**Solution:**

- Add unused packages to the ``excludes`` list
- Use system Python instead of Homebrew/pyenv Python
- Enable stripping and optimization (already default in example)

Can't access files/permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:**

After first launch, grant necessary permissions:

1. Open **System Settings → Privacy & Security**
2. Find the relevant permission (e.g., Full Disk Access)
3. Click **+** and add your ``.app``
4. Restart the app

Complete Example
----------------

See ``examples/packaging_test/screentime.py`` and ``examples/packaging_test/setup_screentime.py`` for a complete working example of a packaged StackIt application.

Resources
---------

- `py2app documentation <https://py2app.readthedocs.io/>`_
- `PyObjC documentation <https://pyobjc.readthedocs.io/>`_
- `Apple Developer - Code Signing <https://developer.apple.com/support/code-signing/>`_
- `examples/packaging_test/BUILD.md <https://github.com/bbalduzz/stackit/blob/main/examples/BUILD.md>`_ - Quick reference
- `examples/packaging_test/PACKAGING.md <https://github.com/bbalduzz/stackit/blob/main/examples/PACKAGING.md>`_ - Detailed guide
