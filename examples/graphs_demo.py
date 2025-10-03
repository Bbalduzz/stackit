#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Comprehensive demonstration of all chart/graph controls in StackIt."""

import stackit
import random


class GraphsDemoApp:
    def __init__(self):
        self.app = stackit.StackApp(
            title="Charts Demo",
            icon=stackit.SFSymbol("chart.bar.fill", rendering="hierarchical"),
        )
        self.setup_ui()

        # Update charts every 2 seconds
        self.timer = stackit.every(2.0, self.update_charts)

    def setup_ui(self):
        # === LINE CHART SECTION ===
        line_chart_item = stackit.MenuItem(
            layout=stackit.vstack(
                [
                    stackit.label("Line Chart", bold=True, font_size=14),
                    stackit.separator(),
                    stackit.hstack(
                        [
                            stackit.vstack(
                                [
                                    stackit.label(
                                        "CPU Usage", font_size=11, color="gray"
                                    ),
                                    stackit.line_chart(
                                        points=[45, 52, 48, 55, 62, 58, 65, 70, 68, 72],
                                        dimensions=(120, 40),
                                        max_value=100.0,
                                        color="#0A84FF",
                                        line_width=1.0,
                                        fill=True,
                                    ),
                                ],
                                spacing=4,
                            ),
                            stackit.spacer(),
                            stackit.vstack(
                                [
                                    stackit.label(
                                        "Network Traffic", font_size=11, color="gray"
                                    ),
                                    stackit.line_chart(
                                        points=[20, 35, 30, 50, 45, 60, 55, 70, 65, 80],
                                        dimensions=(120, 40),
                                        max_value=100.0,
                                        color="#32D74B",
                                        line_width=1.0,
                                        fill=True,
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=16,
                    ),
                    stackit.label(
                        "Smooth spline interpolation with SpriteKit",
                        font_size=9,
                        color="gray",
                    ),
                ],
                spacing=8,
            )
        )
        self.app.add(line_chart_item)

        # === BAR CHART SECTION ===
        bar_chart_item = stackit.MenuItem(
            layout=stackit.vstack(
                [
                    stackit.label("Bar Chart", bold=True, font_size=14),
                    stackit.separator(),
                    stackit.hstack(
                        [
                            stackit.vstack(
                                [
                                    stackit.label("Sales", font_size=11, color="gray"),
                                    stackit.bar_chart(
                                        values=[65, 80, 55, 90, 70, 85, 75],
                                        dimensions=(120, 40),
                                        max_value=100.0,
                                        color="#FF9F0A",
                                        bar_spacing=2.0,
                                        corner_radius=2.0,
                                    ),
                                ],
                                spacing=4,
                            ),
                            stackit.spacer(),
                            stackit.vstack(
                                [
                                    stackit.label(
                                        "Performance", font_size=11, color="gray"
                                    ),
                                    stackit.bar_chart(
                                        values=[40, 55, 70, 60, 75, 65, 80, 70, 85],
                                        dimensions=(120, 40),
                                        max_value=100.0,
                                        color="#BF5AF2",
                                        bar_spacing=1.5,
                                        corner_radius=1.5,
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=16,
                    ),
                    stackit.label(
                        "Customizable bar spacing and corner radius",
                        font_size=9,
                        color="gray",
                    ),
                ],
                spacing=8,
            )
        )
        self.app.add(bar_chart_item)

        # === RING CHART SECTION ===
        ring_chart_item = stackit.MenuItem(
            layout=stackit.vstack(
                [
                    stackit.label("Ring Charts", bold=True, font_size=14),
                    stackit.separator(),
                    stackit.hstack(
                        [
                            stackit.vstack(
                                [
                                    stackit.label(
                                        "Activity Rings", font_size=11, color="gray"
                                    ),
                                    stackit.ring_chart(
                                        data=[85, 65, 45],
                                        dimensions=(100, 100),
                                        colors=["#32D74B", "#0A84FF", "#FF375F"],
                                        ring_width=10.0,
                                        spacing=2.5,
                                        labels=["Move", "Exercise", "Stand"],
                                    ),
                                    stackit.label(
                                        "85% / 65% / 45%", font_size=9, color="gray"
                                    ),
                                ],
                                spacing=4,
                            ),
                            stackit.spacer(),
                            stackit.vstack(
                                [
                                    stackit.label(
                                        "Progress Goals", font_size=11, color="gray"
                                    ),
                                    stackit.ring_chart(
                                        data=[90, 70, 50, 30],
                                        dimensions=(100, 100),
                                        colors=[
                                            "#FFD60A",
                                            "#FF9F0A",
                                            "#FF453A",
                                            "#BF5AF2",
                                        ],
                                        ring_width=8.0,
                                        spacing=2.0,
                                        labels=["Q1", "Q2", "Q3", "Q4"],
                                    ),
                                    stackit.label(
                                        "Quarterly goals", font_size=9, color="gray"
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=16,
                    ),
                    stackit.label(
                        "Multi-ring donut charts with custom colors",
                        font_size=9,
                        color="gray",
                    ),
                ],
                spacing=8,
            )
        )
        self.app.add(ring_chart_item)

        # === COMPACT CHARTS SECTION ===
        self.compact_item = stackit.MenuItem()
        self.app.add(self.compact_item)
        self.update_compact_charts()

    def update_compact_charts(self):
        """Update the compact charts section."""
        # Generate random data
        line_data = [random.randint(20, 80) for _ in range(8)]
        bar_data = [random.randint(30, 90) for _ in range(6)]
        ring_data = [random.randint(50, 95) for _ in range(3)]

        layout = stackit.vstack(
            [
                stackit.label("Compact Charts", bold=True, font_size=14),
                stackit.separator(),
                stackit.hstack(
                    [
                        stackit.vstack(
                            [
                                stackit.label("Mini Line", font_size=10, color="gray"),
                                stackit.line_chart(
                                    points=line_data,
                                    dimensions=(60, 20),
                                    max_value=100.0,
                                    color="#FF453A",
                                    line_width=0.5,
                                    fill=True,
                                ),
                            ],
                            spacing=2,
                        ),
                        stackit.spacer(),
                        stackit.vstack(
                            [
                                stackit.label("Mini Bar", font_size=10, color="gray"),
                                stackit.bar_chart(
                                    values=bar_data,
                                    dimensions=(60, 20),
                                    max_value=100.0,
                                    color="#5E5CE6",
                                    bar_spacing=1.0,
                                    corner_radius=1.0,
                                ),
                            ],
                            spacing=2,
                        ),
                        stackit.spacer(),
                        stackit.vstack(
                            [
                                stackit.label("Mini Ring", font_size=10, color="gray"),
                                stackit.ring_chart(
                                    data=ring_data,
                                    dimensions=(60, 60),
                                    ring_width=6.0,
                                    spacing=1.5,
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=12,
                ),
                stackit.label(
                    "Live updating mini charts (updates every 2s)",
                    font_size=9,
                    color="gray",
                ),
            ],
            spacing=8,
        )

        self.compact_item.set_layout(layout)

    def update_charts(self, timer):
        """Update charts with new random data."""
        # Update only the compact charts section
        self.update_compact_charts()

        # Force menu to redraw
        self.app.update()

    def run(self):
        self.app.run()


if __name__ == "__main__":
    GraphsDemoApp().run()
