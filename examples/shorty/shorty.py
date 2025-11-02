#!/usr/bin/env python3
"""
Shorty - Minimal Global Shortcuts using StackIt
A simple menu bar app for user-defined global shortcuts with minimal UI.
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Any

try:
    from pynput import keyboard
    from pynput.keyboard import GlobalHotKeys

    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("Warning: pynput not available. Install with: pip install pynput")

import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import stackit


class ShortyApp:
    """Minimal shortcut manager with global hotkeys and simple UI."""

    def __init__(self):
        self.app = None
        self.hotkey_listener = None
        self.config_dir = Path.home() / ".config" / "shorty"
        self.shortcuts_file = self.config_dir / "shortcuts.json"
        self.shortcuts: Dict[str, Dict[str, Any]] = {}
        self.load_shortcuts()

        # Default shortcuts if none exist
        if not self.shortcuts:
            self.shortcuts = {
                "<cmd>+<enter>": {
                    "name": "Terminal",
                    "action": "terminal",
                    "key_display": "\r",
                },
                "<cmd>+<shift>+f": {
                    "name": "Finder",
                    "action": "finder",
                    "key_display": ("shift", "f"),
                },
                "<cmd>+<shift>+s": {
                    "name": "Sublime Text",
                    "action": "sublime",
                    "key_display": ("shift", "s"),
                },
                "<cmd>+<shift>+b": {
                    "name": "Safari",
                    "action": "safari",
                    "key_display": ("shift", "s"),
                },
                "<cmd>+<shift>+x": {
                    "name": "Firefox",
                    "action": "firefox",
                    "key_display": ("shift", "x"),
                },
            }
            self.save_shortcuts()

    def load_shortcuts(self):
        """Load shortcuts from config file."""
        try:
            if self.shortcuts_file.exists():
                with open(self.shortcuts_file, "r") as f:
                    self.shortcuts = json.load(f)
        except Exception as e:
            print(f"Error loading shortcuts: {e}")
            self.shortcuts = {}

    def save_shortcuts(self):
        """Save shortcuts to config file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.shortcuts_file, "w") as f:
                json.dump(self.shortcuts, f, indent=2)
        except Exception as e:
            print(f"Error saving shortcuts: {e}")

    def start_hotkey_listener(self):
        """Start the global hotkey listener."""
        if not PYNPUT_AVAILABLE:
            return

        if self.hotkey_listener:
            self.hotkey_listener.stop()

        # Build hotkey mapping
        hotkey_map = {}
        for hotkey, config in self.shortcuts.items():
            action = config["action"]
            hotkey_map[hotkey] = lambda a=action: self.execute_action(a)

        try:
            self.hotkey_listener = GlobalHotKeys(hotkey_map)
            self.hotkey_listener.start()
            print(f"Started global hotkeys: {list(hotkey_map.keys())}")
        except Exception as e:
            print(f"Error starting hotkey listener: {e}")

    def execute_action(self, action: str):
        """Execute the specified action."""
        print(f"Executing: {action}")

        shortcuts_map = {
            "terminal": "terminal",
            "finder": "finder",
            "sublime": r"sublime\ text",
            "safari": "safari",
            "firefox": "firefox",
        }

        subprocess.run(
            f"source ~/.zshrc && launch {shortcuts_map[action]}",
            shell=True,
            executable="/bin/zsh",
        )

    def build_menu(self):
        """Build the menu with shortcuts."""
        # Add each shortcut as a MenuItem for display only (no callback)
        for hotkey, config in self.shortcuts.items():
            name = config.get("name", f"Shortcut")
            key_display = config.get("key_display", "")

            item = stackit.MenuItem(
                title=name,
                key_equivalent=key_display,
            )
            self.app.add(item)

        # Add management options
        self.app.add_separator()
        self.app.add(
            stackit.MenuItem(
                title="Open Config File",
                callback=lambda s: subprocess.run(["open", str(self.shortcuts_file)]),
            )
        )

    def parse_hotkey_for_display(self, hotkey):
        """Parse hotkey string to display format."""
        # Simple parsing - convert common patterns
        hotkey_lower = hotkey.lower()

        if "<cmd>+<shift>+" in hotkey_lower:
            key = hotkey_lower.split("<cmd>+<shift>+")[-1].strip("<>")
            return ["shift", key]
        elif "<cmd>+<alt>+" in hotkey_lower or "<cmd>+<option>+" in hotkey_lower:
            key = hotkey_lower.split("+")[-1].strip("<>")
            return ["alt", key]
        elif "<cmd>+" in hotkey_lower:
            key = hotkey_lower.split("<cmd>+")[-1].strip("<>")
            return key

        return hotkey  # Fallback

    def run(self):
        """Run the application."""
        # Create StackIt app
        self.app = stackit.StackApp(
            icon=stackit.SFSymbol(
                "command.square.fill", rendering="hierarchical", scale="large"
            ),
        )

        # Build initial menu
        self.build_menu()

        # Start global hotkeys
        if PYNPUT_AVAILABLE:
            self.start_hotkey_listener()
        else:
            print("pynput not available - global hotkeys disabled")

        # Run the app
        self.app.run()

        # Cleanup
        if self.hotkey_listener:
            self.hotkey_listener.stop()


def main():
    """Main entry point."""
    app = ShortyApp()
    app.run()


if __name__ == "__main__":
    main()
