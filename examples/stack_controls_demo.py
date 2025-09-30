#!/usr/bin/env python3
"""
Demo showing the new slider, checkbox, and combobox controls in StackMenuItem.
"""

from inspect import stack
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import stackbar

class StackControlsDemo:
    def __init__(self):
        # Create the StackApp instance first to initialize NSApplication
        self.app = stackbar.StackApp(title="Demo")

    def setup_menu(self):
        # Create a StackMenuItem with all three new controls after app is initialized
        self.create_controls_menu()

    def create_controls_menu(self):
        """Create a menu item demonstrating all the new controls."""
        # Create the stack menu item
        stack_item = stackbar.StackMenuItem("Settings Panel")

        # Create main vertical stack with title
        title = stack_item.hstack(
            controls = [
                stackbar.image(stackbar.SFSymbol("ev.plug.dc.chademo")),
                stackbar.label("Control Panel", font_size=16, bold=True),
                stackbar.spacer(),
                stackbar.link(text="help", url="https://github.com")
                # stackbar.image(stackbar.SFSymbol("moonphase.waxing.crescent"))
            ]
        )
        # title = stackbar.label("Control Panel", font_size=16, bold=True)

        # Volume slider section
        volume_section = stack_item.hstack(
            controls=[
                stackbar.label("Volume:"),
                stackbar.slider(
                    value=75,
                    min_value=0,
                    max_value=100,
                    width=150,
                    callback=self.volume_changed
                )
            ]
        )

        # Checkbox section
        checkbox_section = stack_item.vstack(
            controls=[
                stackbar.checkbox(
                    title="Enable Notifications",
                    checked=True,
                    callback=self.notifications_toggled
                ),
                stackbar.checkbox(
                    title="Launch at startup",
                    checked=False,
                    callback=self.auto_launch_toggled
                )
            ],
            spacing=6.0
        )

        # Theme selection section
        theme_section = stack_item.hstack(
            controls=[
                stackbar.label("Theme:"),
                stackbar.combobox(
                    items=["Light", "Dark", "Auto"],
                    selected_index=0,
                    width=120,
                    callback=self.theme_changed
                )
            ]
        )

        # Quality selection (editable combobox)
        quality_section = stack_item.hstack(
            controls=[
                stackbar.label("Quality:"),
                stackbar.combobox(
                    items=["720p", "1080p", "1440p", "4K"],
                    selected_index=1,
                    width=100,
                    editable=True,
                    callback=self.quality_changed
                )
            ]
        )

        # Progress bar section
        progress_section = stack_item.vstack(
            controls=[
                stackbar.label("Progress:"),
                stack_item.vstack(
                    controls=[
                        stackbar.progress_bar(indeterminate=True),
                        stackbar.progress_bar(value=0.6, show_text=True)
                    ]
                )
            ],
            spacing=35
        )

        # Circular progress section
        circular_progress_section = stack_item.vstack(
            controls=[
                stackbar.label("Circular Progress:"),
                stack_item.hstack(
                    controls=[
                        stackbar.circular_progress(
                            indeterminate=True,
                            dimensions=(20, 20)
                        ),
                        stackbar.circular_progress(
                            value=0.35,
                            dimensions=(20, 20)
                        )
                    ]
                ),
                stackbar.spacer()
            ],
            spacing=30
        )

        contact_section = stack_item.vstack(
              controls=[
                  stackbar.label("Name:"),
                  stackbar.text_field(placeholder="Full name"),
                  stackbar.label("password:"),
                  stackbar.secure_text_input(placeholder="Email address"),
                  stackbar.label("Seach document:"),
                  stackbar.search_field(action="searchFieldAction:")
              ],
              spacing=8
          )

        pickers_section = stack_item.vstack(
            controls=[
                stackbar.label("Pickers:"),
                stack_item.hstack(
                    controls = [
                        stackbar.date_picker(callback=self.date_changed),
                        stackbar.time_picker(callback=self.time_changed)
                    ]
                )
            ]
        )

        # Create main vertical stack with all sections
        main_stack = stack_item.vstack(
            controls=[
                title,
                volume_section,
                checkbox_section,
                theme_section,
                quality_section,
                progress_section,
                circular_progress_section,
                contact_section,
                pickers_section
            ],
            spacing=12.0
        )

        # Set the root stack
        stack_item.set_root_stack(main_stack)

        # Add to menu
        self.app.add_item("settings", stack_item)

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