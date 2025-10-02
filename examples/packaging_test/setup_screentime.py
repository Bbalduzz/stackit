"""
py2app setup script for ScreenTime Tracker

Usage:
    python setup_screentime.py py2app

This will create a standalone .app bundle in the dist/ folder.
"""

from setuptools import setup
import sys
import os

# Add parent directory to path so stackit can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

APP = ['screentime.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,  # Don't emulate command line arguments
    'iconfile': None,  # Optional: path to .icns file for app icon
    'plist': {
        'CFBundleName': 'ScreenTime',
        'CFBundleDisplayName': 'ScreenTime Tracker',
        'CFBundleIdentifier': 'com.stackit.screentime',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        'LSMinimumSystemVersion': '10.15.0',  # macOS Catalina (for Knowledge DB)
        'LSUIElement': True,  # Run as menu bar app (no dock icon)
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,  # Support dark mode
        # Request Full Disk Access in System Preferences
        'NSAppleEventsUsageDescription': 'ScreenTime needs to read app usage data.',
        'NSSystemAdministrationUsageDescription': 'ScreenTime needs Full Disk Access to read screen time data.',
    },
    'packages': [
        'stackit',  # Use 'stackit' not 'stackitui' (import name)
        'AppKit',
        'Foundation',
        'objc',
        'sqlite3',
        'httpx',
        'certifi',  # Required by httpx
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
    'strip': True,  # Strip debug symbols to reduce size
    'optimize': 2,  # Maximum optimization
}

setup(
    name='ScreenTime',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
