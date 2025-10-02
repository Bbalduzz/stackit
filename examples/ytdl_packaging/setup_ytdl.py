"""
py2app setup script for YouTube Downloader

Usage:
    python setup_ytdl.py py2app -A

This will create a standalone .app bundle in the dist/ folder.
"""

from setuptools import setup
import sys
import os

# Add parent directory to path so stackit can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

APP = ['yt.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,
    'plist': {
        'CFBundleName': 'YouTubeDL',
        'CFBundleDisplayName': 'YouTube Downloader',
        'CFBundleIdentifier': 'com.stackit.youtubedl',
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
        'pytubefix',
        'httpx',
        'certifi',
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
    name='YouTubeDL',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
