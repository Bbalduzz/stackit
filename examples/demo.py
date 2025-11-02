#!/usr/bin/env python3
"""
Complete StackIt Controls Demo
===============================
This demo showcases EVERY control available in StackIt with ALL their variants.
Controls are organized into submenus by category for easy exploration.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
import stackit
import datetime
from AppKit import NSDatePickerStyleClockAndCalendar, NSDatePickerStyleTextFieldAndStepper


class AllControlsDemo:
    def __init__(self):
        self.app = stackit.StackApp(
            title="Controls Demo",
            icon=stackit.SFSymbol("rectangle.3.group", rendering="hierarchical", color="#007AFF")
        )

    def setup_menu(self):
        """Build comprehensive menu with submenus for each control category."""

        # Main menu items with submenus for each category
        # Using SF Symbols in layouts instead of emoji
        self.app.add(stackit.MenuItem(
            layout=stackit.hstack([
                stackit.image(stackit.SFSymbol("textformat", color="#007AFF"), width=16, height=16),
                stackit.label("Labels & Text"),
            ], spacing=6.0),
            submenu=self.create_label_submenu()
        ))

        self.app.add(stackit.MenuItem(
            layout=stackit.hstack([
                stackit.image(stackit.SFSymbol("button.horizontal", color="#007AFF"), width=16, height=16),
                stackit.label("Buttons"),
            ], spacing=6.0),
            submenu=self.create_button_submenu()
        ))

        self.app.add(stackit.MenuItem(
            layout=stackit.hstack([
                stackit.image(stackit.SFSymbol("keyboard", color="#007AFF"), width=16, height=16),
                stackit.label("Text Inputs"),
            ], spacing=6.0),
            submenu=self.create_text_input_submenu()
        ))

        self.app.add(stackit.MenuItem(
            layout=stackit.hstack([
                stackit.image(stackit.SFSymbol("checklist", color="#007AFF"), width=16, height=16),
                stackit.label("Selection Controls"),
            ], spacing=6.0),
            submenu=self.create_selection_submenu()
        ))

        self.app.add(stackit.MenuItem(
            layout=stackit.hstack([
                stackit.image(stackit.SFSymbol("calendar", color="#007AFF"), width=16, height=16),
                stackit.label("Date & Time"),
            ], spacing=6.0),
            submenu=self.create_datetime_submenu()
        ))

        self.app.add(stackit.MenuItem(
            layout=stackit.hstack([
                stackit.image(stackit.SFSymbol("chart.bar.fill", color="#007AFF"), width=16, height=16),
                stackit.label("Progress Indicators"),
            ], spacing=6.0),
            submenu=self.create_progress_submenu()
        ))

        self.app.add(stackit.MenuItem(
            layout=stackit.hstack([
                stackit.image(stackit.SFSymbol("chart.xyaxis.line", color="#007AFF"), width=16, height=16),
                stackit.label("Charts"),
            ], spacing=6.0),
            submenu=self.create_chart_submenu()
        ))

        self.app.add(stackit.MenuItem(
            layout=stackit.hstack([
                stackit.image(stackit.SFSymbol("play.rectangle", color="#007AFF"), width=16, height=16),
                stackit.label("Media Controls"),
            ], spacing=6.0),
            submenu=self.create_media_submenu()
        ))

        self.app.add(stackit.MenuItem(
            layout=stackit.hstack([
                stackit.image(stackit.SFSymbol("rectangle.3.group", color="#007AFF"), width=16, height=16),
                stackit.label("Layout"),
            ], spacing=6.0),
            submenu=self.create_layout_submenu()
        ))

        self.app.add_separator()

        # Standalone window demo
        self.app.add(stackit.MenuItem(
            layout=stackit.hstack([
                stackit.image(stackit.SFSymbol("macwindow", color="#007AFF"), width=16, height=16),
                stackit.label("Open Demo Window"),
            ], spacing=6.0),
            callback=self.open_window
        ))

    # ==================== SUBMENU 1: LABELS ====================

    def create_label_submenu(self):
        """Create submenu showcasing all label variants."""
        return [
            stackit.MenuItem(
                title="Basic Labels ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Default label (13pt, regular)"),
                        stackit.label("Bold label", bold=True),
                        stackit.label("Large label", font_size=16),
                        stackit.label("Small label", font_size=11),
                        stackit.label("Tiny label", font_size=9),
                    ], spacing=4.0))
                ]
            ),
            stackit.MenuItem(
                title="Colored Labels ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Red", color="#FF3B30"),
                        stackit.label("Orange", color="#FF9500"),
                        stackit.label("Yellow", color="#FFD60A"),
                        stackit.label("Green", color="#34C759"),
                        stackit.label("Blue", color="#007AFF"),
                        stackit.label("Purple", color="#AF52DE"),
                    ], spacing=4.0))
                ]
            ),
            stackit.MenuItem(
                title="Wrapping Labels ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label(
                            "This is a long wrapping label that demonstrates text wrapping when content exceeds menu width.",
                            wraps=True, width=250, max_lines=3, font_size=11
                        ),
                    ], spacing=6.0))
                ]
            ),
            stackit.MenuItem(
                title="Links ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.link("StackIt on GitHub", "https://github.com/Bbalduzz/stackit"),
                        stackit.link("Python.org", "https://python.org"),
                    ], spacing=4.0))
                ]
            ),
        ]

    # ==================== SUBMENU 2: BUTTONS ====================

    def create_button_submenu(self):
        """Create submenu showcasing all button variants."""
        return [
            stackit.MenuItem(
                title="Button Styles ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("All Button Styles:", bold=True),
                        stackit.button("Default", callback=self.btn_click, style="default"),
                        stackit.button("Rounded", callback=self.btn_click, style="rounded"),
                        stackit.button("Inline", callback=self.btn_click, style="inline"),
                        stackit.button("Textured", callback=self.btn_click, style="textured"),
                        stackit.button("Rounded Rect", callback=self.btn_click, style="rounded-rect"),
                        stackit.button("Recessed", callback=self.btn_click, style="recessed"),
                    ], spacing=6.0))
                ]
            ),
            stackit.MenuItem(
                title="Buttons with Icons ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Image Positions:", bold=True),
                        stackit.button(
                            "Left",
                            callback=self.btn_click,
                            image=stackit.SFSymbol("arrow.left"),
                            image_position="left"
                        ),
                        stackit.button(
                            "Right",
                            callback=self.btn_click,
                            image=stackit.SFSymbol("arrow.right"),
                            image_position="right"
                        ),
                        stackit.button(
                            "Above",
                            callback=self.btn_click,
                            image=stackit.SFSymbol("arrow.up"),
                            image_position="above"
                        ),
                        stackit.label("Icon Only:", bold=True),
                        stackit.hstack([
                            stackit.button(None, callback=self.btn_click,
                                         image=stackit.SFSymbol("heart.fill", color="#FF3B30"),
                                         image_position="only", style="rounded"),
                            stackit.button(None, callback=self.btn_click,
                                         image=stackit.SFSymbol("star.fill", color="#FFD60A"),
                                         image_position="only", style="rounded"),
                            stackit.button(None, callback=self.btn_click,
                                         image=stackit.SFSymbol("bolt.fill", color="#FF9500"),
                                         image_position="only", style="rounded"),
                        ], spacing=8.0),
                    ], spacing=6.0))
                ]
            ),
        ]

    # ==================== SUBMENU 3: TEXT INPUTS ====================

    def create_text_input_submenu(self):
        """Create submenu showcasing all text input variants."""
        return [
            stackit.MenuItem(
                title="Text Fields ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Regular Text Field:", bold=True),
                        stackit.text_field(placeholder="Enter your name", size=(250, 25)),
                        stackit.label("Wide Text Field:", bold=True),
                        stackit.text_field(placeholder="Wide field", size=(300, 30)),
                    ], spacing=6.0))
                ]
            ),
            stackit.MenuItem(
                title="Secure Input ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Password Input:", bold=True),
                        stackit.secure_text_input(placeholder="Enter password", width=250),
                        stackit.secure_text_input(placeholder="Confirm password", width=250),
                    ], spacing=6.0))
                ]
            ),
            stackit.MenuItem(
                title="Search Field ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Search:", bold=True),
                        stackit.search_field(placeholder="Search...", size=(250, 25)),
                    ], spacing=6.0))
                ]
            ),
        ]

    # ==================== SUBMENU 4: SELECTION CONTROLS ====================

    def create_selection_submenu(self):
        """Create submenu showcasing selection controls."""
        return [
            stackit.MenuItem(
                title="Checkboxes ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.checkbox("Option 1", checked=True, callback=self.checkbox_changed),
                        stackit.checkbox("Option 2", checked=False, callback=self.checkbox_changed),
                        stackit.checkbox("Option 3", checked=True, callback=self.checkbox_changed),
                    ], spacing=4.0))
                ]
            ),
            stackit.MenuItem(
                title="Radio Buttons ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Horizontal:", bold=True),
                        stackit.radio_group(
                            options=["Small", "Medium", "Large"],
                            selected=1,
                            orientation="horizontal",
                            callback=lambda s: print(f"Size: {s.title()}")
                        ),
                        stackit.label("Vertical:", bold=True),
                        stackit.radio_group(
                            options=["Red", "Green", "Blue"],
                            selected=0,
                            orientation="vertical",
                            callback=lambda s: print(f"Color: {s.title()}")
                        ),
                    ], spacing=8.0))
                ]
            ),
            stackit.MenuItem(
                title="Sliders ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Volume:", bold=True),
                        stackit.hstack([
                            stackit.label("0"),
                            stackit.slider(value=50, min_value=0, max_value=100, width=200,
                                         callback=lambda s: print(f"Value: {s.doubleValue():.0f}")),
                            stackit.label("100"),
                        ], spacing=8.0),
                        stackit.label("Brightness:", bold=True),
                        stackit.slider(value=75, min_value=0, max_value=100, width=200),
                    ], spacing=8.0))
                ]
            ),
            stackit.MenuItem(
                title="Combobox (Dropdown) ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Non-editable:", bold=True),
                        stackit.combobox(
                            items=["Option A", "Option B", "Option C"],
                            selected_index=0,
                            width=200
                        ),
                        stackit.label("Editable:", bold=True),
                        stackit.combobox(
                            items=["720p", "1080p", "1440p", "4K"],
                            selected_index=1,
                            width=150,
                            editable=True
                        ),
                    ], spacing=6.0))
                ]
            ),
        ]

    # ==================== SUBMENU 5: DATE & TIME ====================

    def create_datetime_submenu(self):
        """Create submenu showcasing date and time pickers."""
        return [
            stackit.MenuItem(
                title="Date Pickers ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Clock & Calendar:", bold=True),
                        stackit.date_picker(
                            style=NSDatePickerStyleClockAndCalendar,
                            callback=lambda s: print(f"Date: {s.dateValue()}")
                        ),
                        stackit.label("TextField & Stepper:", bold=True),
                        stackit.date_picker(
                            style=NSDatePickerStyleTextFieldAndStepper,
                            size=(200, 25)
                        ),
                    ], spacing=8.0))
                ]
            ),
            stackit.MenuItem(
                title="Time Pickers ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Time Picker:", bold=True),
                        stackit.time_picker(
                            style=NSDatePickerStyleTextFieldAndStepper,
                            callback=lambda s: print(f"Time: {s.dateValue()}")
                        ),
                    ], spacing=6.0))
                ]
            ),
        ]

    # ==================== SUBMENU 6: PROGRESS ====================

    def create_progress_submenu(self):
        """Create submenu showcasing progress indicators."""
        return [
            stackit.MenuItem(
                title="Progress Bars ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Determinate:", bold=True),
                        stackit.progress_bar(value=0.35, dimensions=(250, 20), show_text=True),
                        stackit.progress_bar(value=0.65, dimensions=(250, 20), show_text=True, color="#34C759"),
                        stackit.progress_bar(value=0.85, dimensions=(250, 20), show_text=True, color="#FF9500"),
                        stackit.label("Indeterminate:", bold=True),
                        stackit.progress_bar(indeterminate=True, dimensions=(250, 20)),
                    ], spacing=8.0))
                ]
            ),
        ]

    # ==================== SUBMENU 7: CHARTS ====================

    def create_chart_submenu(self):
        """Create submenu showcasing charts."""
        return [
            stackit.MenuItem(
                title="Line Charts ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Basic Line Chart:", bold=True),
                        stackit.line_chart(
                            points=[20, 35, 28, 45, 55, 48, 62, 58, 72],
                            dimensions=(280, 60),
                            max_value=100.0,
                            color="#007AFF",
                            line_width=2.0,
                            fill=True
                        ),
                        stackit.label("With Axes & Grid:", bold=True),
                        stackit.line_chart(
                            points=[45, 52, 48, 55, 62, 58, 65, 70],
                            dimensions=(280, 80),
                            max_value=100.0,
                            color="#34C759",
                            line_width=1.5,
                            fill=True,
                            show_axes=True,
                            show_grid=True,
                            x_labels=["Jan", "Feb", "Mar", "Apr"],
                            y_labels=[0, 50, 100]
                        ),
                    ], spacing=8.0))
                ]
            ),
            stackit.MenuItem(
                title="Bar Charts ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Basic Bar Chart:", bold=True),
                        stackit.bar_chart(
                            values=[30, 45, 60, 55, 70, 65],
                            dimensions=(280, 60),
                            max_value=100.0,
                            color="#FF9500",
                            bar_spacing=3.0,
                            corner_radius=2.0
                        ),
                        stackit.label("With Axes:", bold=True),
                        stackit.bar_chart(
                            values=[30, 45, 60, 55, 70, 65],
                            dimensions=(280, 80),
                            max_value=100.0,
                            color="#AF52DE",
                            show_axes=True,
                            show_grid=True,
                            x_labels=["A", "B", "C", "D", "E", "F"],
                            y_labels=[0, 50, 100]
                        ),
                    ], spacing=8.0))
                ]
            ),
            stackit.MenuItem(
                title="Ring Charts ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Activity Rings:", bold=True),
                        stackit.hstack([
                            stackit.ring_chart(
                                data=[85, 65, 45],
                                dimensions=(80, 80),
                                colors=["#FF375F", "#0A84FF", "#32D74B"],
                                ring_width=8.0
                            ),
                            stackit.ring_chart(
                                data=[90, 70, 50, 30],
                                dimensions=(80, 80),
                                colors=["#FFD60A", "#FF9F0A", "#FF453A", "#BF5AF2"],
                                ring_width=6.0
                            ),
                        ], spacing=20.0),
                    ], spacing=8.0))
                ]
            ),
        ]

    # ==================== SUBMENU 8: MEDIA ====================

    def create_media_submenu(self):
        """Create submenu showcasing media controls."""
        return [
            stackit.MenuItem(
                title="Video Player ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("AVKit Video Player:", bold=True),
                        stackit.video(
                            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                            dimensions=(320, 180),
                            show_controls=True,
                            border_radius=8.0
                        ),
                    ], spacing=6.0))
                ]
            ),
            stackit.MenuItem(
                title="Map View ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("MapKit Map:", bold=True),
                        stackit.map_view(
                            latitude=37.7749,
                            longitude=-122.4194,
                            zoom=0.05,
                            dimensions=(320, 200),
                            map_type="standard",
                            show_controls=True,
                            border_radius=8.0,
                            annotations=[{
                                'latitude': 37.7749,
                                'longitude': -122.4194,
                                'title': 'San Francisco',
                                'subtitle': 'California'
                            }]
                        ),
                    ], spacing=6.0))
                ]
            ),
            stackit.MenuItem(
                title="Web View ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("WebKit Web View:", bold=True),
                        stackit.web_view(
                            html="""
                            <html>
                            <body style="font-family: -apple-system; padding: 20px; text-align: center;">
                                <h2 style="color: #007AFF;">Hello from WebKit!</h2>
                                <p>Embedded web content</p>
                            </body>
                            </html>
                            """,
                            dimensions=(300, 100),
                            border_radius=8.0
                        ),
                    ], spacing=6.0))
                ]
            ),
        ]

    # ==================== SUBMENU 9: LAYOUT ====================

    def create_layout_submenu(self):
        """Create submenu showcasing layout helpers."""
        return [
            stackit.MenuItem(
                title="Stacks ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("HStack (Horizontal):", bold=True),
                        stackit.hstack([
                            stackit.label("Left"),
                            stackit.spacer(),
                            stackit.label("Right"),
                        ]),
                        stackit.separator(),
                        stackit.label("VStack (Vertical):", bold=True),
                        stackit.vstack([
                            stackit.label("First"),
                            stackit.label("Second"),
                            stackit.label("Third"),
                        ], spacing=2.0),
                    ], spacing=8.0))
                ]
            ),
            stackit.MenuItem(
                title="Separators ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("Horizontal Separator:", bold=True),
                        stackit.separator(vertical=False),
                        stackit.label("Vertical Separator:", bold=True),
                        stackit.hstack([
                            stackit.label("Left"),
                            stackit.separator(vertical=True),
                            stackit.label("Right"),
                        ]),
                    ], spacing=8.0))
                ]
            ),
            stackit.MenuItem(
                title="Block Container ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.block(
                            stackit.vstack([
                                stackit.label("Rounded Block", bold=True, color="#007AFF"),
                                stackit.label("Content with border and background"),
                                stackit.button("OK", callback=self.btn_click, style="default"),
                            ], spacing=6.0),
                            radius=8.0,
                            padding=12.0
                        ),
                    ], spacing=8.0))
                ]
            ),
            stackit.MenuItem(
                title="Images ▶",
                submenu=[
                    stackit.MenuItem(layout=stackit.vstack([
                        stackit.label("SF Symbols:", bold=True),
                        stackit.hstack([
                            stackit.image(stackit.SFSymbol("star.fill", color="#FFD60A"), width=24, height=24),
                            stackit.image(stackit.SFSymbol("heart.fill", color="#FF3B30"), width=24, height=24),
                            stackit.image(stackit.SFSymbol("bolt.fill", color="#FF9500"), width=24, height=24),
                        ], spacing=12.0),
                    ], spacing=6.0))
                ]
            ),
        ]

    # ==================== CALLBACKS ====================

    def btn_click(self, sender):
        """Handle button clicks."""
        title = sender.title() if sender.title() else "Icon Button"
        print(f"Button clicked: {title}")

    def checkbox_changed(self, sender):
        """Handle checkbox state changes."""
        state = "checked" if sender.state() == 1 else "unchecked"
        print(f"Checkbox '{sender.title()}' {state}")

    def open_window(self, sender):
        """Open a standalone window with controls."""
        # UI operations must run on main thread
        import AppKit

        def create_window_on_main_thread():
            win = stackit.window(title="Settings", size=(400, 350))

            content = stackit.vstack([
                stackit.label("Application Settings", bold=True, font_size=16),
                stackit.separator(),
                stackit.hstack([
                    stackit.label("Username:", width=100),
                    stackit.text_field(placeholder="Enter username", size=(250, 25)),
                ], spacing=10.0),
                stackit.hstack([
                    stackit.label("Password:", width=100),
                    stackit.secure_text_input(placeholder="Enter password", width=250),
                ], spacing=10.0),
                stackit.checkbox("Remember me", checked=True),
                stackit.checkbox("Enable notifications"),
                stackit.hstack([
                    stackit.label("Theme:", width=100),
                    stackit.combobox(items=["Light", "Dark", "Auto"], selected_index=0, width=150),
                ], spacing=10.0),
                stackit.spacer(),
                stackit.hstack([
                    stackit.spacer(),
                    stackit.button("Cancel", callback=lambda s: self.close_window_on_main_thread(win), style="rounded"),
                    stackit.button("Save", callback=lambda s: self.save_settings(win), style="default"),
                ], spacing=10.0),
            ], spacing=12.0)

            stackit.window_layout(win, content, padding=(20, 20, 20, 20))
            win.makeKeyAndOrderFront_(None)

        # Dispatch to main thread
        AppKit.NSOperationQueue.mainQueue().addOperationWithBlock_(create_window_on_main_thread)

    def close_window_on_main_thread(self, window):
        """Close window on main thread."""
        import AppKit
        AppKit.NSOperationQueue.mainQueue().addOperationWithBlock_(lambda: window.close())

    def save_settings(self, window):
        """Save settings and close window."""
        import AppKit

        def save_on_main_thread():
            print("Settings saved!")
            stackit.notification("Settings", "Your settings have been saved")
            window.close()

        AppKit.NSOperationQueue.mainQueue().addOperationWithBlock_(save_on_main_thread)

    def run(self):
        """Start the application."""
        self.setup_menu()

        print("\n" + "=" * 70)
        print("StackIt - Complete Controls Demo (Organized with Submenus)")
        print("=" * 70)
        print("\nAll controls are organized into submenus by category:")
        print("\n  Labels & Text - Basic, colored, wrapping labels, links")
        print("  Buttons - 7 styles, with icons, icon-only")
        print("  Text Inputs - Text field, secure, search")
        print("  Selection - Checkboxes, radio, sliders, comboboxes")
        print("  Date & Time - Date pickers, time pickers")
        print("  Progress - Bars (determinate/indeterminate)")
        print("  Charts - Line, bar, ring charts")
        print("  Media - Video, maps, web views")
        print("  Layout - Stacks, separators, blocks, images")
        print("  Windows - Standalone window demo")
        print("\n" + "=" * 70 + "\n")

        self.app.run()


if __name__ == "__main__":
    demo = AllControlsDemo()
    demo.run()
