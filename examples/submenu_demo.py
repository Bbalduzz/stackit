#!/usr/bin/env python3
"""
Demo showing submenu functionality in StackIt.
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import stackit

class SubmenuDemo:
    def __init__(self):
        # Create the app
        self.app = stackit.StackApp(
            title="Submenu Demo",
            icon=stackit.SFSymbol("square.grid.3x1.folder.badge.plus", rendering="hierarchical")
        )

        self.setup_menu()

    def setup_menu(self):
        # Simple submenu example
        simple_submenu = [
            stackit.MenuItem(
                layout=stackit.hstack(
                    [
                        stackit.label("test"),
                        stackit.spacer(),
                        stackit.image(stackit.SFSymbol("testtube.2", rendering="hierarchical"))
                    ]
                ),
                callback=lambda s: print("Option 3 selected")
            ),
            stackit.MenuItem(title="Option 1", key_equivalent="1", callback=lambda s: print("Option 1 selected")),
            stackit.MenuItem(title="Option 2", key_equivalent="2", callback=lambda s: print("Option 2 selected")),
        ]

        simple_item = stackit.MenuItem(
            title="Simple Submenu",
            key_equivalent="s",
            submenu=simple_submenu
        )
        self.app.add(simple_item)

        # Nested submenu example
        nested_level_2 = [
            stackit.MenuItem(title="Sub-option A", callback=lambda s: print("A selected")),
            stackit.MenuItem(title="Sub-option B", callback=lambda s: print("B selected")),
            stackit.MenuItem(title="Sub-option C", callback=lambda s: print("C selected")),
        ]

        nested_level_1 = [
            stackit.MenuItem(title="File Operations", submenu=[
                stackit.MenuItem(title="New", callback=lambda s: print("New")),
                stackit.MenuItem(title="Open", callback=lambda s: print("Open")),
                stackit.MenuItem(title="Save", callback=lambda s: print("Save")),
            ]),
            stackit.MenuItem(title="Edit Operations", submenu=[
                stackit.MenuItem(title="Cut", callback=lambda s: print("Cut")),
                stackit.MenuItem(title="Copy", callback=lambda s: print("Copy")),
                stackit.MenuItem(title="Paste", callback=lambda s: print("Paste")),
            ]),
            'separator',
            stackit.MenuItem(title="More Options ▶", submenu=nested_level_2),
        ]

        nested_item = stackit.MenuItem(
            title="Nested Submenu",
            submenu=nested_level_1
        )
        self.app.add(nested_item)

        # Settings submenu with mixed content
        settings_submenu = [
            stackit.MenuItem(title="Preferences...", callback=self.show_preferences, key_equivalent=","),
            stackit.MenuItem(title="Accounts", submenu=[
                stackit.MenuItem(title="Add Account", callback=lambda s: print("Add account")),
                stackit.MenuItem(title="Remove Account", callback=lambda s: print("Remove account")),
            ]),
            'separator',
            stackit.MenuItem(title="Advanced", submenu=[
                stackit.MenuItem(title="Clear Cache", callback=lambda s: print("Cache cleared")),
                stackit.MenuItem(title="Reset Settings", callback=lambda s: print("Settings reset")),
            ]),
        ]

        settings_item = stackit.MenuItem(
            title="Settings",
            submenu=settings_submenu
        )
        self.app.add(settings_item)

        # Add separator
        self.app.add_separator()

        # Regular menu item with custom layout
        layout = stackit.hstack([
            stackit.label("Status:", bold=True),
            stackit.spacer(),
            stackit.label("Ready", color="#00FF00")
        ])

        self.app.add(stackit.MenuItem(layout=layout))

    def show_preferences(self, sender):
        """Show preferences dialog."""
        stackit.alert("Preferences", "Preferences dialog would open here", ok="OK")
        print("Preferences opened")

    def run(self):
        """Start the application."""
        self.app.run()

if __name__ == "__main__":
    demo = SubmenuDemo()
    demo.run()
