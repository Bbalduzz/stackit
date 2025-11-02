#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test thread-safe timer functionality
"""

import os
import sys
import threading

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
import stackit


class TimerTestApp:
    def __init__(self):
        self.app = stackit.StackApp(title="Timer Test")
        self.counter = 0

        # Create a label to update
        self.status_item = stackit.MenuItem()
        self.app.add(self.status_item, key="status")

        # Test button
        self.app.add(
            stackit.MenuItem(
                title="Test Background Thread Timer",
                callback=self.test_background_timer
            )
        )

        self.update_ui()

    def update_ui(self):
        """Update the UI with current counter."""
        layout = stackit.vstack([
            stackit.label(f"Counter: {self.counter}", bold=True),
            stackit.label("(Updates from background thread)", font_size=10, color="#8E8E93")
        ], spacing=4.0)

        self.status_item.set_layout(layout)
        self.app.update()

    def test_background_timer(self, sender=None):
        """Test calling stackit.after() from a background thread."""
        print("Starting background thread test...")

        def background_task():
            print("Background thread started")
            # Simulate some work
            import time
            time.sleep(1)

            # This should now work without crashes!
            print("Calling stackit.after() from background thread...")
            stackit.after(0.0, self.increment_counter)
            print("stackit.after() called successfully from background thread")

        threading.Thread(target=background_task, daemon=True).start()

    def increment_counter(self, timer):
        """Increment counter and update UI (called on main thread)."""
        print(f"increment_counter called on main thread")
        self.counter += 1
        self.update_ui()
        print(f"Counter updated to {self.counter}")

    def run(self):
        """Start the application."""
        self.app.run()


if __name__ == "__main__":
    app = TimerTestApp()
    app.run()
