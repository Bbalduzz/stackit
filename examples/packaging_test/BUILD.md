# Quick Build Guide

## TL;DR - Build ScreenTime.app

```bash
# 1. Install py2app
pip install py2app

# 2. Make sure stackit is installed
cd /path/to/stackit
pip install -e .

# 3. Build in alias mode (faster, for development)
cd examples
python setup_screentime.py py2app -A

# 4. Run
open dist/ScreenTime.app
```

## Grant Permissions

After first launch:
1. **System Settings** → **Privacy & Security** → **Full Disk Access**
2. Click **+** and add `ScreenTime.app`
3. Restart the app

## File Sizes

- Source: `screentime.py` (~15 KB)
- Built app: `ScreenTime.app` (~50-100 MB)
  - Includes Python runtime, PyObjC, and all dependencies

## Common Commands

```bash
# Development build (faster, links to source) - RECOMMENDED
python setup_screentime.py py2app -A

# Clean and rebuild
rm -rf build dist
python setup_screentime.py py2app -A

# Full standalone build (for distribution)
# Note: May have issues with editable installs, use alias mode instead
python setup_screentime.py py2app

# Create distributable ZIP
cd dist
zip -r ScreenTime.zip ScreenTime.app

# Test the app
open dist/ScreenTime.app

# Check app info
ls -lh dist/ScreenTime.app
```

## Troubleshooting

**ImportError: No module named 'stackit'?**
- Make sure stackit is installed: `pip install -e /path/to/stackit`
- Use alias mode for development: `python setup_screentime.py py2app -A`

**App won't launch?**
- Check Console.app for errors
- Ensure you built in alias mode: `python setup_screentime.py py2app -A`

**Module not found?**
- Add to `packages` list in `setup_screentime.py`

**Can't access database?**
- Grant Full Disk Access in System Settings

**App too large?**
- Add unused packages to `excludes` list
- Use system Python instead of Homebrew

See [PACKAGING.md](PACKAGING.md) for detailed instructions.
