#!/usr/bin/env python3
"""
Demo showing block containers with borders and backgrounds (CPU monitor design).
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import stackit


class ActivityMonitor:
    def __init__(self):
        self.app = stackit.StackApp(title="Activity", icon=stackit.SFSymbol("desktopcomputer.trianglebadge.exclamationmark", rendering="hierarchical"))
        self.setup_ui()

    def create_cpu_header(self):
        """Create CPU header with percentage and chart."""
        return stackit.hstack([
            stackit.label("CPU", bold=True, font_size=16),
            stackit.spacer(),
            stackit.label("26%", font_size=16),
            # Mini chart with spline interpolation
            stackit.line_chart(
                points=[10, 15, 8, 20, 18, 25, 22, 26, 24, 26],
                dimensions=(60, 20),
                max_value=100.0,
                line_width=1.0,
                fill=True
            )
        ])

    def create_cpu_stats_row(self):
        """Create CPU stats row with System, User, Nice, and Temp."""
        return stackit.hstack([
            stackit.vstack([
                stackit.label("System", font_size=10, color="gray"),
                stackit.label("8.6%", font_size=14)
            ], alignment=None),
            stackit.spacer(),
            stackit.vstack([
                stackit.label("User", font_size=10, color="gray"),
                stackit.label("17.7%", font_size=14)
            ], alignment=None),
            stackit.spacer(),
            stackit.vstack([
                stackit.label("Nice", font_size=10, color="gray"),
                stackit.label("0.0%", font_size=14)
            ], alignment=None),
            stackit.spacer(),
            stackit.vstack([
                stackit.label("Temp", font_size=10, color="gray"),
                stackit.label("63°C", font_size=14)
            ], alignment=None)
        ])

    def create_process_row(self, name, cpu):
        """Create a process row with name, CPU usage, and control buttons."""
        return stackit.hstack([
            stackit.label(name, font_size=13, color="gray"),
            stackit.spacer(),
            stackit.label(cpu, font_size=13),
            # Pause icon button
            stackit.button(
                image=stackit.SFSymbol("pause.circle", point_size=14, color="gray"),
                image_position="only",
                style="default"
            ),
            # Close icon button
            stackit.button(
                image=stackit.SFSymbol("xmark.circle", point_size=14, color="gray"),
                image_position="only",
                style="default"
            )
        ])

    def create_process_list(self):
        """Create list of processes with their CPU usage."""
        return stackit.vstack([
            self.create_process_row("systemstats", "114.9"),
            self.create_process_row("WindowServer", "31.1"),
            self.create_process_row("Figma Helper (Renderer).app", "14.5"),
            self.create_process_row("sysmond", "14.1"),
            self.create_process_row("kernel_task", "5.8"),
        ], spacing=6)

    def setup_ui(self):
        """Set up the UI layout."""
        cpu_content = stackit.vstack([
            self.create_cpu_header(),
            stackit.separator(),
            self.create_cpu_stats_row(),
            stackit.separator(),
            self.create_process_list()
        ], spacing=12)

        # Wrap in block
        cpu_block = stackit.block(
            cpu_content,
            radius=8.0,
            padding=(16, 16, 16, 16),
            # border_color="#FFFFFF20",  # Subtle white border
            # background_color="#00000040"  # Dark semi-transparent background
        )

        item = stackit.MenuItem(layout=cpu_block)
        self.app.add(item)

    def run(self):
        """Run the application."""
        self.app.run()


if __name__ == "__main__":
    monitor = ActivityMonitor()
    monitor.run()
