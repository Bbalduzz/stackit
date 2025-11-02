#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Demonstration of chart controls with axes and grid support."""

import os, sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
import stackit


def main():
    app = stackit.StackApp(
        title="Charts with Axes",
        icon=stackit.SFSymbol("chart.xyaxis.line", rendering="hierarchical"),
    )

    # === LINE CHART WITH AXES ===
    line_with_axes = stackit.MenuItem(
        layout=stackit.vstack(
            [
                stackit.label("Line Chart with Axes", bold=True, font_size=14),
                stackit.separator(),
                stackit.line_chart(
                    points=[45, 52, 48, 55, 62, 58, 65, 70, 68, 72],
                    dimensions=(250, 120),
                    max_value=100.0,
                    min_value=0.0,
                    color="#0A84FF",
                    line_width=1.5,
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
                    ],
                    y_labels=[0, 25, 50, 75, 100],
                ),
                stackit.label(
                    "With grid lines and axis labels",
                    font_size=9,
                    color="gray",
                ),
            ],
            spacing=8,
        )
    )
    app.add(line_with_axes)

    # === BAR CHART WITH AXES ===
    bar_with_axes = stackit.MenuItem(
        layout=stackit.vstack(
            [
                stackit.label("Bar Chart with Axes", bold=True, font_size=14),
                stackit.separator(),
                stackit.bar_chart(
                    values=[65, 80, 55, 90, 70, 85, 75],
                    dimensions=(250, 120),
                    max_value=100.0,
                    min_value=0.0,
                    color="#32D74B",
                    bar_spacing=2.0,
                    corner_radius=2.0,
                    show_axes=True,
                    show_grid=True,
                    x_labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                    y_labels=[0, 50, 100],
                ),
                stackit.label(
                    "Weekly performance metrics",
                    font_size=9,
                    color="gray",
                ),
            ],
            spacing=8,
        )
    )
    app.add(bar_with_axes)

    # === CHART WITH AXES ONLY (NO GRID) ===
    axes_only = stackit.MenuItem(
        layout=stackit.vstack(
            [
                stackit.label("Axes Without Grid", bold=True, font_size=14),
                stackit.separator(),
                stackit.line_chart(
                    points=[20, 35, 30, 50, 45, 60, 55, 70, 65, 80],
                    dimensions=(250, 100),
                    max_value=100.0,
                    color="#FF9F0A",
                    line_width=1.5,
                    fill=True,
                    show_axes=True,
                    show_grid=False,
                    x_labels=["Q1", "Q2", "Q3", "Q4"],
                    y_labels=[0, 50, 100],
                ),
                stackit.label(
                    "Quarterly revenue growth",
                    font_size=9,
                    color="gray",
                ),
            ],
            spacing=8,
        )
    )
    app.add(axes_only)

    # === CUSTOM COLORS ===
    custom_colors = stackit.MenuItem(
        layout=stackit.vstack(
            [
                stackit.label("Custom Axis Colors", bold=True, font_size=14),
                stackit.separator(),
                stackit.bar_chart(
                    values=[30, 45, 60, 55, 70, 65],
                    dimensions=(220, 100),
                    max_value=100.0,
                    color="#BF5AF2",
                    bar_spacing=3.0,
                    corner_radius=2.0,
                    show_axes=True,
                    show_grid=True,
                    x_labels=["A", "B", "C", "D", "E", "F"],
                    y_labels=[0, 25, 50, 75, 100],
                    axis_color="#BF5AF2",
                    grid_color="#BF5AF240",
                ),
                stackit.label(
                    "Purple theme with matching grid",
                    font_size=9,
                    color="gray",
                ),
            ],
            spacing=8,
        )
    )
    app.add(custom_colors)

    # === COMPACT CHARTS COMPARISON ===
    comparison = stackit.MenuItem(
        layout=stackit.vstack(
            [
                stackit.label("With vs Without Axes", bold=True, font_size=14),
                stackit.separator(),
                stackit.hstack(
                    [
                        stackit.vstack(
                            [
                                stackit.label("Without", font_size=10, color="gray"),
                                stackit.line_chart(
                                    points=[40, 55, 50, 65, 60, 75],
                                    dimensions=(100, 50),
                                    max_value=100.0,
                                    color="#FF453A",
                                    line_width=1.0,
                                    fill=True,
                                ),
                            ],
                            spacing=4,
                        ),
                        stackit.vstack(
                            [
                                stackit.label("With axes", font_size=10, color="gray"),
                                stackit.line_chart(
                                    points=[40, 55, 50, 65, 60, 75],
                                    dimensions=(130, 70),
                                    max_value=100.0,
                                    color="#FF453A",
                                    line_width=1.0,
                                    fill=True,
                                    show_axes=True,
                                    x_labels=["A", "B", "C", "D", "E", "F"],
                                    y_labels=[0, 50, 100],
                                ),
                            ],
                            spacing=4,
                        ),
                    ],
                    spacing=12,
                ),
                stackit.label(
                    "Side-by-side comparison",
                    font_size=9,
                    color="gray",
                ),
            ],
            spacing=8,
        )
    )
    app.add(comparison)

    app.run()


if __name__ == "__main__":
    main()
