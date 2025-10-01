#!/usr/bin/env python3
"""
Demo showing the new slider, checkbox, and combobox controls in StackMenuItem.
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import stackit

class StackControlsDemo:
    def __init__(self):
        # Create the StackApp instance first to initialize NSApplication
        self.app = stackit.StackApp(title="Controls", icon=stackit.SFSymbol("figure.walk.motion.trianglebadge.exclamationmark", rendering="hierarchical"))

    def setup_menu(self):
        # Create a StackMenuItem with all three new controls after app is initialized
        self.create_controls_menu()

    def create_controls_menu(self):
        """Create a menu item demonstrating all the new controls."""
        # Title section
        title = stackit.hstack([
            stackit.image(stackit.SFSymbol("ev.plug.dc.chademo")),
            stackit.label("Control Panel", font_size=16, bold=True),
            stackit.spacer(),
            stackit.link(text="help", url="https://github.com")
        ])

        # Volume slider section
        volume_section = stackit.hstack([
            stackit.label("Volume:"),
            stackit.slider(
                value=75,
                min_value=0,
                max_value=100,
                width=150,
                callback=self.volume_changed
            )
        ])

        # Checkbox section
        checkbox_section = stackit.vstack([
            stackit.checkbox(
                title="Enable Notifications",
                checked=True,
                callback=self.notifications_toggled
            ),
            stackit.checkbox(
                title="Launch at startup",
                checked=False,
                callback=self.auto_launch_toggled
            )
        ], spacing=6.0)

        # Theme selection section
        theme_section = stackit.hstack([
            stackit.label("Theme:"),
            stackit.combobox(
                items=["Light", "Dark", "Auto"],
                selected_index=0,
                width=120,
                callback=self.theme_changed
            )
        ])

        # Quality selection (editable combobox)
        quality_section = stackit.hstack([
            stackit.label("Quality:"),
            stackit.combobox(
                items=["720p", "1080p", "1440p", "4K"],
                selected_index=1,
                width=100,
                editable=True,
                callback=self.quality_changed
            )
        ])

        # Progress bar section
        progress_section = stackit.vstack([
            stackit.label("Progress:"),
            stackit.vstack([
                stackit.progress_bar(indeterminate=True),
                stackit.progress_bar(value=0.6, show_text=True)
            ])
        ], spacing=35)

        # Circular progress section
        circular_progress_section = stackit.vstack([
            stackit.label("Circular Progress:"),
            stackit.hstack([
                stackit.circular_progress(
                    indeterminate=True,
                    dimensions=(20, 20)
                ),
                stackit.circular_progress(
                    value=0.35,
                    dimensions=(20, 20)
                )
            ]),
            stackit.spacer()
        ], spacing=30)

        contact_section = stackit.vstack([
            stackit.label("Name:"),
            stackit.text_field(placeholder="Full name"),
            stackit.label("password:"),
            stackit.secure_text_input(placeholder="Email address"),
            stackit.label("Seach document:"),
            stackit.search_field(action="searchFieldAction:")
        ], spacing=8)

        pickers_section = stackit.vstack([
            stackit.label("Pickers:"),
            stackit.hstack([
                stackit.date_picker(callback=self.date_changed),
                stackit.time_picker(callback=self.time_changed)
            ])
        ])

        # Create menu item with layout directly
        stack_item = stackit.MenuItem(layout=stackit.vstack([
            title,
            volume_section,
            checkbox_section,
            theme_section,
            quality_section,
            progress_section,
            circular_progress_section,
            contact_section,
            pickers_section
        ], spacing=12.0))

        # Add to menu
        self.app.add(stack_item)

    def run(self):
        """Start the application."""
        # Setup menu after app is initialized but before running
        self.setup_menu()
        self.app.run()

    def searchFieldAction_(self, sender):
        """Handle serach field action"""
        print("Search field:", sender.stringValue())

    def volume_changed(self, sender):
        """Callback for volume slider changes."""
        value = sender.doubleValue()
        print(f"Volume slider changed to: {value}")

    def notifications_toggled(self, sender):
        """Callback for notifications checkbox."""
        state = sender.state()
        checked = state == 1  # NSControlStateValueOn = 1
        print(f"Notifications checkbox toggled: {'ON' if checked else 'OFF'}")

    def auto_launch_toggled(self, sender):
        """Callback for auto-launch checkbox."""
        state = sender.state()
        checked = state == 1
        print(f"Auto-launch checkbox toggled: {'ON' if checked else 'OFF'}")

    def theme_changed(self, sender):
        """Callback for theme combobox selection."""
        index = sender.indexOfSelectedItem()
        value = sender.stringValue()
        print(f"Theme selection changed to index {index}: '{value}'")

    def quality_changed(self, sender):
        """Callback for quality combobox selection."""
        index = sender.indexOfSelectedItem()
        value = sender.stringValue()
        print(f"Quality selection changed to index {index}: '{value}'")

    def date_changed(self, sender):
        """Callback for date picker changes."""
        date_value = sender.dateValue()
        print(f"Date picker changed to: {date_value}")

    def time_changed(self, sender):
        """Callback for time picker changes."""
        time_value = sender.dateValue()
        print(f"Time picker changed to: {time_value}")

if __name__ == "__main__":
    demo = StackControlsDemo()
    demo.run()