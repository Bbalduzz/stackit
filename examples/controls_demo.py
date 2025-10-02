#!/usr/bin/env python3
"""
Comprehensive demo showcasing all StackIt features:
- Custom layouts with all UI controls
- Simple text menu items with keyboard shortcuts
- Submenus (nested menus)
- Badges (macOS 14.0+)
- Dynamic updates
- SF Symbols
- Timers
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import stackit

class ComprehensiveDemo:
    def __init__(self):
        # Create app with SF Symbol icon
        self.app = stackit.StackApp(
            title="Demo",
            icon=stackit.SFSymbol("sparkles", rendering="hierarchical", color="#FF6B35")
        )

        # State for dynamic updates
        self.notification_count = 3
        self.timer_count = 0
        self.volume = 75
        self.notifications_enabled = True

    def setup_menu(self):
        """Build the complete menu structure."""

        # ========== SECTION 1: Custom Layout with Controls ==========
        self.create_controls_panel()

        self.app.add_separator()

        # ========== SECTION 2: Dynamic Content (updates via timer) ==========
        self.create_dynamic_section()

        self.app.add_separator()

        # ========== SECTION 3: Simple Menu Items ==========
        # Preferences menu item with keyboard shortcut
        prefs_item = stackit.MenuItem(
            title="Preferences...",
            callback=self.show_preferences,
            key_equivalent=","  # ⌘,
        )
        self.app.add(prefs_item)

        # About menu item
        about_item = stackit.MenuItem(
            title="About StackIt",
            callback=self.show_about
        )
        self.app.add(about_item)

        self.app.add_separator()

        # ========== SECTION 4: Submenus ==========
        self.create_submenus()

        self.app.add_separator()

        # ========== SECTION 5: Menu Items with Badges ==========
        # Notifications with badge showing count
        self.notifications_item = stackit.MenuItem(
            title="Notifications",
            callback=self.show_notifications
        )
        self.notifications_item.set_badge("new-items", count=self.notification_count)
        self.app.add(self.notifications_item, key="notifications")

        # Updates available badge
        updates_item = stackit.MenuItem(
            title="Updates Available",
            callback=self.check_updates,
            badge="updates"
        )
        self.app.add(updates_item)

        # Start timer for dynamic updates
        stackit.every(2.0, self.update_dynamic_content)

    def create_controls_panel(self):
        """Create a rich custom layout showing all available controls."""

        # Header with icon and title
        header = stackit.hstack([
            stackit.image(stackit.SFSymbol("slider.horizontal.3", rendering="hierarchical")),
            stackit.label("Control Panel", font_size=16, bold=True),
            stackit.spacer(),
            stackit.link(text="Help", url="https://github.com/Bbalduzz/stackit")
        ])

        # ========== Input Controls Block ==========
        self.volume_label = stackit.label(f"{self.volume}%", color="#888888")
        input_controls = stackit.block(
            stackit.vstack([
                stackit.label("Input Controls", bold=True, color="#FF6B35"),
                # Slider
                stackit.hstack([
                    stackit.label("Volume:"),
                    stackit.slider(
                        value=self.volume,
                        min_value=0,
                        max_value=100,
                        width=150,
                        callback=self.volume_changed
                    ),
                    self.volume_label
                ]),
                # Checkboxes
                stackit.vstack([
                    stackit.checkbox(
                        title="Enable Notifications",
                        checked=self.notifications_enabled,
                        callback=self.notifications_toggled
                    ),
                    stackit.checkbox(
                        title="Launch at Startup",
                        checked=False,
                        callback=self.auto_launch_toggled
                    ),
                    stackit.checkbox(
                        title="Dark Mode",
                        checked=True,
                        callback=self.dark_mode_toggled
                    )
                ], spacing=6.0),
                # Comboboxes
                stackit.hstack([
                    stackit.label("Theme:"),
                    stackit.combobox(
                        items=["Light", "Dark", "Auto"],
                        selected_index=2,
                        width=120,
                        callback=self.theme_changed
                    )
                ]),
                stackit.hstack([
                    stackit.label("Quality:"),
                    stackit.combobox(
                        items=["720p", "1080p", "1440p", "4K"],
                        selected_index=1,
                        width=100,
                        editable=True,
                        callback=self.quality_changed
                    )
                ])
            ], spacing=8.0),
            radius=8.0
        )

        # ========== Progress Indicators Block ==========
        progress_block = stackit.block(
            stackit.vstack([
                stackit.label("Progress Indicators", bold=True, color="#4ECDC4", width=150),
                # Linear progress bars
                stackit.hstack([
                    stackit.label("Loading:"),
                    stackit.progress_bar(value=0.65, show_text=True, dimensions=(150, 20))
                ]),
                stackit.hstack([
                    stackit.label("Processing:"),
                    stackit.progress_bar(indeterminate=True, dimensions=(150, 20))
                ]),
                # Circular progress
                stackit.hstack([
                    stackit.label("Circular:"),
                    stackit.circular_progress(value=0.35, dimensions=(20, 20)),
                    stackit.circular_progress(indeterminate=True, dimensions=(20, 20)),
                    stackit.spacer()
                ])
            ], spacing=8.0),
            radius=8.0
        )

        # ========== Text Fields Block ==========
        text_fields_block = stackit.block(
            stackit.vstack([
                stackit.label("Text Input", bold=True, color="#95E1D3"),
                stackit.text_field(placeholder="Enter your name"),
                stackit.secure_text_input(placeholder="Enter password"),
                stackit.search_field(action="searchFieldAction:")
            ], spacing=6.0),
            radius=8.0
        )

        # ========== Date & Time Block ==========
        datetime_block = stackit.block(
            stackit.vstack([
                stackit.label("Date & Time Pickers", bold=True, color="#F38181"),
                stackit.hstack([
                    stackit.date_picker(callback=self.date_changed),
                    stackit.time_picker(callback=self.time_changed)
                ])
            ], spacing=6.0),
            radius=8.0
        )

        # ========== Charts Block ==========
        # Sample data for line chart
        chart_data = [20, 35, 28, 45, 55, 48, 62, 58, 72, 68, 80, 75]
        charts_block = stackit.block(
            stackit.vstack([
                stackit.label("Data Visualization", bold=True, color="#A8E6CF"),
                stackit.hstack([
                    stackit.label("CPU Usage:"),
                    stackit.line_chart(
                        points=chart_data,
                        dimensions=(180, 40),
                        max_value=100.0,
                        min_value=0.0,
                        line_width=2.0
                    )
                ])
            ], spacing=8.0),
            radius=8.0
        )

        # ========== Action Buttons ==========
        button_section = stackit.hstack([
            stackit.button("Save", action="saveAction:"),
            stackit.button("Cancel", action="cancelAction:"),
            stackit.spacer()
        ])

        # Combine all blocks
        layout = stackit.vstack([
            header,
            input_controls,
            progress_block,
            text_fields_block,
            datetime_block,
            charts_block,
            button_section
        ], spacing=12.0)

        # Create menu item with the layout
        controls_item = stackit.MenuItem(layout=layout)
        self.app.add(controls_item, key="controls")

    def create_dynamic_section(self):
        """Create a section that updates dynamically via timer."""
        self.timer_label = stackit.label(f"Timer: {self.timer_count}s", color="#4ECDC4")
        self.status_label = stackit.label("● Active", color="#00FF00")

        dynamic_layout = stackit.hstack([
            stackit.image(stackit.SFSymbol("clock.fill", rendering="hierarchical", color="#4ECDC4")),
            self.timer_label,
            stackit.spacer(),
            self.status_label
        ])

        self.dynamic_item = stackit.MenuItem(layout=dynamic_layout)
        self.app.add(self.dynamic_item, key="dynamic")

    def create_submenus(self):
        """Create nested submenus to demonstrate submenu feature."""

        # Tools submenu
        tools_submenu = [
            stackit.MenuItem(title="Calculator", callback=lambda s: print("Calculator")),
            stackit.MenuItem(title="Terminal", callback=lambda s: print("Terminal")),
            'separator',
            stackit.MenuItem(title="Activity Monitor", callback=lambda s: print("Activity Monitor"))
        ]

        # Export submenu (nested inside File submenu)
        export_submenu = [
            stackit.MenuItem(title="Export as PDF", callback=lambda s: print("Export PDF")),
            stackit.MenuItem(title="Export as PNG", callback=lambda s: print("Export PNG")),
            stackit.MenuItem(title="Export as SVG", callback=lambda s: print("Export SVG"))
        ]

        # File submenu with nested Export submenu
        file_submenu = [
            stackit.MenuItem(title="New File", callback=lambda s: print("New File"), key_equivalent="n"),
            stackit.MenuItem(title="Open...", callback=lambda s: print("Open"), key_equivalent="o"),
            'separator',
            stackit.MenuItem(title="Export ▶", submenu=export_submenu),
            'separator',
            stackit.MenuItem(title="Close", callback=lambda s: print("Close"), key_equivalent="w")
        ]

        # View submenu with custom layout inside
        view_layout = stackit.hstack([
            stackit.label("Zoom:"),
            stackit.slider(value=100, min_value=50, max_value=200, width=100, callback=self.zoom_changed),
            stackit.label("100%")
        ])
        view_custom_item = stackit.MenuItem(layout=view_layout)

        view_submenu = [
            stackit.MenuItem(title="Zoom In", callback=lambda s: print("Zoom In"), key_equivalent="+"),
            stackit.MenuItem(title="Zoom Out", callback=lambda s: print("Zoom Out"), key_equivalent="-"),
            'separator',
            view_custom_item
        ]

        # Create main menu items with submenus
        file_menu = stackit.MenuItem(title="File", submenu=file_submenu)
        view_menu = stackit.MenuItem(title="View", submenu=view_submenu)
        tools_menu = stackit.MenuItem(title="Tools", submenu=tools_submenu)
        image_menu = stackit.MenuItem(title="Image", submenu=[
            stackit.MenuItem(
                layout=stackit.hstack([
                    stackit.image("https://i.redd.it/y0eiummi1irf1.jpeg", width=200, border_radius=8)
                ]),
                badge="1"
            )
        ])

        self.app.add(file_menu)
        self.app.add(view_menu)
        self.app.add(tools_menu)
        self.app.add(image_menu)

    # ========== Callbacks ==========

    def update_dynamic_content(self, timer):
        """Update dynamic content periodically."""
        self.timer_count += 2

        # Update labels
        self.timer_label = stackit.label(f"Timer: {self.timer_count}s", color="#4ECDC4")

        # Alternate status
        if (self.timer_count // 2) % 2 == 0:
            self.status_label = stackit.label("● Active", color="#00FF00")
        else:
            self.status_label = stackit.label("● Idle", color="#888888")

        # Update layout
        new_layout = stackit.hstack([
            stackit.image(stackit.SFSymbol("clock.fill", rendering="hierarchical", color="#4ECDC4")),
            self.timer_label,
            stackit.spacer(),
            self.status_label
        ])

        self.dynamic_item.set_layout(new_layout)
        self.app.update()  # Force menu to redraw

    def searchFieldAction_(self, sender):
        """Handle search field input."""
        print(f"Search: {sender.stringValue()}")

    def volume_changed(self, sender):
        """Update volume display."""
        self.volume = int(sender.doubleValue())
        print(f"Volume: {self.volume}%")

        # Update the volume label in the controls panel
        # Note: For full update, you'd recreate the layout
        # This is simplified for demo purposes

    def notifications_toggled(self, sender):
        """Toggle notifications."""
        self.notifications_enabled = sender.state() == 1
        print(f"Notifications: {'ON' if self.notifications_enabled else 'OFF'}")

        if not self.notifications_enabled:
            # Clear badge when notifications disabled
            self.notifications_item.set_badge(None)
        else:
            # Restore badge
            self.notifications_item.set_badge("new-items", count=self.notification_count)

    def auto_launch_toggled(self, sender):
        print(f"Auto-launch: {'ON' if sender.state() == 1 else 'OFF'}")

    def dark_mode_toggled(self, sender):
        print(f"Dark Mode: {'ON' if sender.state() == 1 else 'OFF'}")

    def theme_changed(self, sender):
        print(f"Theme: {sender.stringValue()}")

    def quality_changed(self, sender):
        print(f"Quality: {sender.stringValue()}")

    def date_changed(self, sender):
        print(f"Date: {sender.dateValue()}")

    def time_changed(self, sender):
        print(f"Time: {sender.dateValue()}")

    def saveAction_(self, sender):
        print("Save button clicked")
        stackit.notification("Settings Saved", "Your preferences have been saved successfully.")

    def cancelAction_(self, sender):
        print("Cancel button clicked")

    def zoom_changed(self, sender):
        zoom = int(sender.doubleValue())
        print(f"Zoom: {zoom}%")

    def show_preferences(self, sender):
        """Show preferences dialog."""
        print("Opening Preferences...")
        stackit.alert("Preferences", "This is where preferences would be configured.", ok="OK")

    def show_about(self, sender):
        """Show about dialog."""
        print("Showing About...")
        stackit.alert(
            "About StackIt",
            "StackIt v0.2.2\n\nA modern framework for creating beautiful macOS menu bar applications.",
            ok="Close"
        )

    def show_notifications(self, sender):
        """Show notifications panel."""
        print("Opening Notifications...")
        if self.notification_count > 0:
            # Mark as read
            self.notification_count = 0
            self.notifications_item.set_badge(None)
            stackit.notification("Notifications", "All notifications have been marked as read.")

    def check_updates(self, sender):
        """Check for updates."""
        print("Checking for updates...")
        stackit.notification("StackIt Updater", "You are running the latest version.")

    def run(self):
        """Start the application."""
        self.setup_menu()
        print("\n" + "="*60)
        print("StackIt Comprehensive Demo - All Features Showcase")
        print("="*60)
        print("\nFeatures demonstrated:")
        print("  ✓ Custom layouts with all UI controls")
        print("  ✓ Grouped controls using stackit.block()")
        print("  ✓ Line charts for data visualization")
        print("  ✓ Simple text menu items with keyboard shortcuts")
        print("  ✓ Nested submenus (File ▶ Export ▶)")
        print("  ✓ Badges with dynamic counts")
        print("  ✓ Dynamic content updates via timers")
        print("  ✓ SF Symbols with custom rendering")
        print("  ✓ Alerts and notifications")
        print("\nInteract with the menu to see all features in action!")
        print("="*60 + "\n")

        self.app.run()

if __name__ == "__main__":
    demo = ComprehensiveDemo()
    demo.run()
