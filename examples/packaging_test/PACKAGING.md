# Packaging StackIt Apps as macOS .app Bundles

This guide shows how to package StackIt applications (like screentime.py) into standalone macOS `.app` bundles using py2app.

## Prerequisites

1. **Install py2app:**
   ```bash
   pip install py2app
   ```

2. **Ensure stackit is importable:**
   ```bash
   # Option 1: Install stackit in development mode (recommended)
   cd /path/to/stackit
   pip install -e .

   # Option 2: Install from PyPI
   pip install stackitui
   ```

## Building the App

### Step 1: Navigate to examples directory
```bash
cd examples
```

### Step 2: Build the .app bundle

**For development (recommended):**
```bash
python setup_screentime.py py2app -A
```

This creates an alias mode build that:
- Links to source files instead of copying them
- Builds much faster (seconds vs minutes)
- Perfect for development and testing
- Requires Python to be installed on the system

**For distribution (standalone):**
```bash
python setup_screentime.py py2app
```

This creates a full standalone build that:
- Bundles Python, all dependencies, and stackit into the app
- Can be distributed to users without Python installed
- Takes longer to build
- Note: May have issues with editable installs of stackit

### Step 3: Test the app
```bash
open dist/ScreenTime.app
```

## Troubleshooting

### Issue: "Module not found" errors
**Solution:** Add the missing module to the `packages` list in `setup_screentime.py`:
```python
'packages': [
    'stackit',
    'your_missing_module',
    # ...
]
```

### Issue: App doesn't launch
**Solution:** Check the Console.app for error messages:
1. Open Console.app
2. Filter for "ScreenTime"
3. Look for Python tracebacks

**Debug mode:** Build in alias mode for faster testing:
```bash
python setup_screentime.py py2app -A
```
This creates a development version that links to source files instead of copying them.

### Issue: App can't access Knowledge database
**Solution:** After first launch, you need to grant Full Disk Access:
1. Open **System Settings → Privacy & Security → Full Disk Access**
2. Click the **+** button
3. Navigate to your `ScreenTime.app` and add it
4. Restart the app

## Customizing the App

### Add a custom icon
1. Create or download an `.icns` file
2. Update `setup_screentime.py`:
   ```python
   'iconfile': 'path/to/icon.icns',
   ```

### Change app name
Update the plist in `setup_screentime.py`:
```python
'CFBundleName': 'YourAppName',
'CFBundleDisplayName': 'Your App Display Name',
'CFBundleIdentifier': 'com.yourcompany.yourapp',
```

### Reduce app size
The bundled app might be 50-100 MB due to Python and PyObjC. To reduce size:

1. **Remove unnecessary packages:**
   ```python
   'excludes': [
       'tkinter',
       'matplotlib',
       'numpy',
       # Add more unused packages
   ]
   ```

2. **Strip debug symbols** (already enabled):
   ```python
   'strip': True,
   'optimize': 2,
   ```

3. **Use system Python** (advanced):
   Build with the system Python instead of Homebrew/pyenv Python to share frameworks.

## Distribution

### Option 1: Distribute as .app
Simply zip the `ScreenTime.app` folder:
```bash
cd dist
zip -r ScreenTime.zip ScreenTime.app
```

Users can unzip and drag to `/Applications`.

### Option 2: Create a DMG installer
Use `create-dmg` or `hdiutil`:

```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "ScreenTime Installer" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "ScreenTime.app" 175 120 \
  --hide-extension "ScreenTime.app" \
  --app-drop-link 425 120 \
  "ScreenTime.dmg" \
  "dist/"
```

### Option 3: Code signing (for distribution outside App Store)
To avoid "unidentified developer" warnings:

```bash
# Sign the app
codesign --deep --force --sign "Developer ID Application: Your Name" dist/ScreenTime.app

# Verify signature
codesign --verify --verbose dist/ScreenTime.app

# Notarize with Apple (requires Apple Developer account)
xcrun notarytool submit ScreenTime.zip --apple-id your@email.com --wait
```

## Creating Setup Files for Other Apps

To package any StackIt app, create a `setup_yourapp.py`:

```python
from setuptools import setup

APP = ['yourapp.py']
OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'CFBundleName': 'YourApp',
        'CFBundleDisplayName': 'Your App Name',
        'CFBundleIdentifier': 'com.yourcompany.yourapp',
        'CFBundleVersion': '1.0.0',
        'LSUIElement': True,  # Menu bar app
    },
    'packages': ['stackit', 'AppKit', 'Foundation', 'objc'],
    'includes': [
        'stackit.core',
        'stackit.controls',
        'stackit.sfsymbol',
        'stackit.utils',
        'stackit.delegate',
    ],
}

setup(
    name='YourApp',
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

Then build:
```bash
python setup_yourapp.py py2app
```

## Tips

- **Development:** Use `-A` alias mode for faster iteration
- **Testing:** Test on a clean macOS VM without Python installed
- **Size:** Expect 50-100 MB for StackIt apps (includes Python runtime)
- **Updates:** Users need to replace the entire .app to update
- **Permissions:** Apps inherit permissions from where they're run during development

## Resources

- [py2app documentation](https://py2app.readthedocs.io/)
- [PyObjC documentation](https://pyobjc.readthedocs.io/)
- [StackIt documentation](https://python-stackit.readthedocs.io/)
- [Apple Developer - Code Signing](https://developer.apple.com/support/code-signing/)
