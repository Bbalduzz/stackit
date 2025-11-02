#!/usr/bin/env python3
"""
py2app setup script for Shorty - Global Shortcuts Manager
Usage: python shorty_setup.py py2app
"""

from setuptools import setup
import sys
import os

# Add the parent directories to sys.path to find stackit
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

APP = ["shorty.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleName": "Shorty",
        "CFBundleDisplayName": "Shorty - Global Shortcuts",
        "CFBundleIdentifier": "com.shorty.globalshortcuts",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "LSUIElement": True,  # Run as background app (no dock icon)
        "LSMinimumSystemVersion": "11.0",  # macOS Big Sur for SF Symbols
        "NSHumanReadableCopyright": "Copyright © 2024",
        "NSHighResolutionCapable": True,
    },
    "packages": [
        "stackit",
        "pynput",
    ],
    "includes": [
        "json",
        "pathlib",
        "subprocess",
        "typing",
    ],
    "excludes": [
        # Development and testing
        "unittest",
        "pytest",
        "nose",
        "doctest",
        "pdb",
        # Documentation
        "pydoc",
        "sphinx",
        # GUI frameworks (we only need PyObjC)
        "tkinter",
        "Tkinter",
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
        "wx",
        "wxPython",
        "kivy",
        "pygame",
        # Web frameworks
        "django",
        "flask",
        "tornado",
        "aiohttp",
        "fastapi",
        "urllib3",
        "requests",
        # Scientific computing
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",
        "seaborn",
        "plotly",
        "sklearn",
        "tensorflow",
        "torch",
        "cv2",
        # Database
        "psycopg2",
        "pymongo",
        "sqlalchemy",
        # Heavy networking
        "ftplib",
        "smtplib",
        # Heavy compression
        "bz2",
        "lzma",
        # XML/HTML parsing
        "lxml",
        "beautifulsoup4",
        # Image processing
        "PIL",
        "Pillow",
        "imageio",
        # Crypto (keep essential ones)
        "cryptography",
        # System specific
        "curses",
        "readline",
        "rlcompleter",
        # Heavy async/concurrent
        "concurrent.futures",
        "asyncio",
        # Internationalization
        "gettext",
    ],
    "arch": "universal2",  # Support both Intel and Apple Silicon
    "strip": True,  # Strip debug symbols
    "optimize": 2,  # Optimize bytecode
}

setup(
    name="Shorty",
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
    install_requires=[
        "pyobjc-framework-Cocoa>=9.0",
        "pynput>=1.7.0",
    ],
)
