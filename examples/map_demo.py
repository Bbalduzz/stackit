#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Map View Demo - Demonstrates the map_view() control using MapKit

This example shows how to embed interactive maps in a menu bar app
with different map types, annotations, and locations.
"""

import sys
import os

# Add src directory to path for development
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
import stackit


def main():
    # Create the app
    app = stackit.StackApp(
        title="Maps",
        icon=stackit.SFSymbol("map.fill", color="#4A90E2")
    )

    # San Francisco with annotations
    sf_map = stackit.map_view(
        latitude=37.7749,
        longitude=-122.4194,
        zoom=0.05,
        dimensions=(400, 300),
        map_type="standard",
        show_controls=True,
        border_radius=12.0,
        annotations=[
            {
                'latitude': 37.7749,
                'longitude': -122.4194,
                'title': 'San Francisco',
                'subtitle': 'Golden Gate City'
            },
            {
                'latitude': 37.8199,
                'longitude': -122.4783,
                'title': 'Golden Gate Bridge',
                'subtitle': 'Iconic landmark'
            }
        ]
    )

    sf_item = stackit.MenuItem(
        layout=stackit.vstack([
            stackit.label("San Francisco", bold=True, font_size=14),
            stackit.separator(),
            sf_map,
            stackit.separator(),
            stackit.label("Standard map with annotations", font_size=10, color="gray"),
        ], spacing=8)
    )

    app.add(sf_item)

    # New York - Satellite view
    ny_map = stackit.map_view(
        latitude=40.7128,
        longitude=-74.0060,
        zoom=0.03,
        dimensions=(400, 300),
        map_type="satellite",
        show_controls=True,
        border_radius=12.0,
        annotations=[
            {
                'latitude': 40.7128,
                'longitude': -74.0060,
                'title': 'New York City',
                'subtitle': 'The Big Apple'
            }
        ]
    )

    ny_item = stackit.MenuItem(
        layout=stackit.vstack([
            stackit.label("New York City", bold=True, font_size=14),
            stackit.separator(),
            ny_map,
            stackit.separator(),
            stackit.label("Satellite view", font_size=10, color="gray"),
        ], spacing=8)
    )

    app.add(ny_item)

    # Paris - Hybrid view
    paris_map = stackit.map_view(
        latitude=48.8566,
        longitude=2.3522,
        zoom=0.02,
        dimensions=(400, 300),
        map_type="hybrid",
        show_controls=True,
        border_radius=12.0,
        annotations=[
            {
                'latitude': 48.8584,
                'longitude': 2.2945,
                'title': 'Eiffel Tower',
                'subtitle': 'La Tour Eiffel'
            },
            {
                'latitude': 48.8606,
                'longitude': 2.3376,
                'title': 'Louvre Museum',
                'subtitle': 'World-famous art museum'
            }
        ]
    )

    paris_item = stackit.MenuItem(
        layout=stackit.vstack([
            stackit.label("Paris", bold=True, font_size=14),
            stackit.separator(),
            paris_map,
            stackit.separator(),
            stackit.label("Hybrid view with landmarks", font_size=10, color="gray"),
        ], spacing=8)
    )

    app.add(paris_item)

    # Info item
    info_item = stackit.MenuItem(
        layout=stackit.vstack([
            stackit.label("Map Control Features:", bold=True),
            stackit.label("• Interactive zoom and pan", font_size=11),
            stackit.label("• Multiple map types (standard, satellite, hybrid)", font_size=11),
            stackit.label("• Custom annotations with titles", font_size=11),
            stackit.label("• Powered by MapKit", font_size=11),
        ], spacing=4)
    )

    app.add(info_item)

    # Run the app
    app.run()


if __name__ == '__main__':
    main()
