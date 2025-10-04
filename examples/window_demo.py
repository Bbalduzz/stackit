#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window Demo - Demonstrates the window control in StacKit.

This example shows how to create standalone windows with StacKit controls.
"""

import stackit


def submit_form(sender=None):
    """Handle form submission"""
    stackit.notification("Form Submitted", "Your data has been saved!")


def open_settings_window(sender=None):
    """Open a settings window with various controls"""
    # Create window
    win = stackit.window(size=(400, 350))

    # Create layout with various controls
    content = stackit.vstack(
        [
            stackit.label("User Settings", bold=True, font_size=16),
            stackit.separator(),
            stackit.hstack(
                [
                    stackit.label("Username:", width=100),
                    stackit.text_field(placeholder="Enter username", width=250),
                ],
                spacing=10.0,
            ),
            stackit.hstack(
                [
                    stackit.label("Email:", width=100),
                    stackit.text_field(placeholder="Enter email", width=250),
                ],
                spacing=10.0,
            ),
            stackit.hstack(
                [
                    stackit.label("Password:", width=100),
                    stackit.secure_text_input(placeholder="Enter password", width=250),
                ],
                spacing=10.0,
            ),
            stackit.separator(),
            stackit.checkbox("Enable notifications"),
            stackit.checkbox("Auto-save settings"),
            stackit.spacer(),
            stackit.hstack(
                [
                    stackit.spacer(),
                    stackit.button("Cancel", callback=lambda: win.close()),
                    stackit.button("Save", callback=submit_form),
                ],
                spacing=10.0,
            ),
        ],
        spacing=12.0,
    )

    # Add layout to window
    stackit.window_layout(win, content, padding=(20, 20, 20, 20))

    # Show window
    win.makeKeyAndOrderFront_(None)


def open_chart_window(sender=None):
    """Open a window with charts"""
    win = stackit.window(size=(500, 400))

    content = stackit.vstack(
        [
            stackit.label("Sales Analytics", bold=True, font_size=16),
            stackit.separator(),
            stackit.label("Monthly Revenue", font_size=12),
            stackit.line_chart(
                points=[45, 52, 48, 55, 62, 58, 65, 70, 68, 72, 75, 80],
                dimensions=(460, 120),
                max_value=100.0,
                color="#0A84FF",
                line_width=2.0,
                fill=True,
                show_axes=True,
                show_grid=True,
                x_labels=[
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ],
                y_labels=[0, 25, 50, 75, 100],
            ),
            stackit.spacer(),
            stackit.label("Category Performance", font_size=12),
            stackit.bar_chart(
                values=[65, 80, 45, 90, 55, 70],
                dimensions=(460, 100),
                max_value=100.0,
                color="#32D74B",
                bar_spacing=10.0,
                corner_radius=4.0,
                show_axes=True,
                show_grid=True,
                x_labels=["A", "B", "C", "D", "E", "F"],
                y_labels=[0, 50, 100],
            ),
        ],
        spacing=10.0,
    )

    stackit.window_layout(win, content, padding=(20, 20, 20, 20))
    win.makeKeyAndOrderFront_(None)


def main():
    """Main application entry point"""
    # Create menu bar app
    app = stackit.StackApp(
        title="Window Demo",
        icon=stackit.SFSymbol("square.grid.2x2", color="#0A84FF"),
    )

    # Add menu items to open different windows
    settings_item = stackit.MenuItem(
        title="Open Settings Window...",
        callback=open_settings_window,
        key_equivalent="s",
    )
    app.add(settings_item)

    charts_item = stackit.MenuItem(
        title="Open Analytics Window...",
        callback=open_chart_window,
        key_equivalent="a",
    )
    app.add(charts_item)

    # Add separator
    app.add(stackit.MenuItem(title="-"))

    # Run app
    app.run()


if __name__ == "__main__":
    main()
