#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple test for window control with button callbacks"""

import os, sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
import stackit


def button_clicked(sender):
    """Button click handler"""
    print(f"✅ Button clicked! Sender: {sender}")
    stackit.notification("Button Clicked", "The button callback works!")


def open_test_window(sender=None):
    """Open a simple test window"""
    win = stackit.window(size=(300, 200))

    content = stackit.vstack(
        [
            stackit.label("Click the button to test callbacks:", bold=True),
            stackit.spacer(),
            stackit.button("Test Callback", callback=button_clicked),
        ],
        spacing=12.0,
    )

    stackit.window_layout(win, content)


def main():
    """Main entry point"""
    app = stackit.StackApp(title="Window Test")

    item = stackit.MenuItem(
        title="Open Test Window",
        callback=open_test_window,
    )
    app.add(item)

    app.run()


if __name__ == "__main__":
    main()
