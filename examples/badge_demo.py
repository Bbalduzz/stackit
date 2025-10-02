#!/usr/bin/env python3
"""
Demo showing NSMenuItemBadge functionality in StackIt (macOS 14.0+).
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import stackit

class BadgeDemo:
    def __init__(self):
        # Create the app
        self.app = stackit.StackApp(
            title="Badge Demo",
            icon=stackit.SFSymbol("bell.badge.fill", rendering="hierarchical")
        )

        self.setup_menu()

    def setup_menu(self):
        # Menu item with "updates" badge (no count)
        updates_item = stackit.MenuItem(
            title="Updates Available",
            callback=lambda s: print("Checking for updates..."),
            badge="updates"
        )
        self.app.add(updates_item)

        # Menu item with "new items" badge (no count)
        new_items_item = stackit.MenuItem(
            title="New Messages",
            callback=lambda s: print("Opening messages..."),
            badge="new-items"
        )
        self.app.add(new_items_item)

        # Menu item with "alerts" badge with count
        alerts_item = stackit.MenuItem(
            title="Alerts",
            callback=lambda s: print("Viewing alerts...")
        )
        alerts_item.set_badge("alerts", count=7)
        self.app.add(alerts_item)

        self.app.add_separator()

        # Dynamic badge example - item we can update
        self.dynamic_item = stackit.MenuItem(
            title="Notifications",
            callback=self.toggle_badge
        )
        self.app.add(self.dynamic_item, key="dynamic")
        self.badge_enabled = False

        # Control items
        self.app.add_separator()

        toggle_item = stackit.MenuItem(
            title="Toggle Badge",
            callback=self.toggle_badge,
            key_equivalent="t"
        )
        self.app.add(toggle_item)

        # Submenu with badges
        submenu_with_badges = [
            stackit.MenuItem(title="Inbox", badge="new-items", callback=lambda s: print("Inbox")),
            stackit.MenuItem(title="Spam", badge="alerts", callback=lambda s: print("Spam")),
            'separator',
            stackit.MenuItem(title="Archive", callback=lambda s: print("Archive")),
        ]

        mail_item = stackit.MenuItem(
            title="Mail",
            submenu=submenu_with_badges,
            badge="updates"
        )
        self.app.add(mail_item)

    def toggle_badge(self, sender):
        """Toggle badge on the dynamic item."""
        self.badge_enabled = not self.badge_enabled

        if self.badge_enabled:
            self.dynamic_item.set_badge("new-items", count=3)
            print("Badge enabled with count 3")
        else:
            # Remove badge by setting it to None
            self.dynamic_item.set_badge(None)
            print("Badge removed")

    def run(self):
        """Start the application."""
        print("Badge Demo started (requires macOS 14.0+)")
        print("Note: If you're on macOS < 14.0, badges won't appear")
        self.app.run()

if __name__ == "__main__":
    demo = BadgeDemo()
    demo.run()
