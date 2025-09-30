Installation
============

Requirements
------------

* macOS 11.0 or later (for SF Symbols support)
* Python 3.7+
* PyObjC (usually pre-installed on macOS)

Install from source
-------------------

Clone the repository and install::

    git clone https://github.com/yourusername/stackit.git
    cd stackit
    pip install -e .

Or simply copy the ``stackit`` directory into your project.

Dependencies
------------

stackit has minimal dependencies:

* **PyObjC** - Python-Objective-C bridge for macOS integration

  - Usually pre-installed on macOS system Python
  - If needed: ``pip install pyobjc-framework-Cocoa``

* **httpx** (optional) - For loading images from URLs

  - Install with: ``pip install httpx``
  - Only needed if using ``stackit.image()`` with HTTP/HTTPS URLs

No other dependencies required! stackit is a standalone framework built directly on macOS AppKit.

Verify Installation
-------------------

Test that stackit is working::

    python3 -c "import stackit; print(stackit.__version__)"

If successful, you'll see the version number printed.
