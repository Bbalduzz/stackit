#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo showcasing the new enum-based API design for StackIt.

This example demonstrates the improved type-safe API using enums instead of strings,
while maintaining backward compatibility with the original string-based approach.
"""

import os
import sys

# Add src directory to path for examples
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
import stackit

class EnumDemoApp:
    def __init__(self):
        # Create app with SF Symbol using new enum API
        self.app = stackit.StackApp(
            title="Enum Demo",
            icon=stackit.SFSymbol(
                "gearshape.fill",
                rendering=stackit.SymbolRenderingMode.HIERARCHICAL,  # New enum approach
                scale=stackit.SymbolScale.MEDIUM,                    # New enum approach
                weight=stackit.SymbolWeight.SEMIBOLD,                # New enum approach
                color="#007AFF"
            )
        )

        self.setup_menu()

    def setup_menu(self):
        """Set up the menu with examples of new enum-based API."""

        # Badge demo using new enum
        badge_item = stackit.MenuItem(
            title="New Features Available",
            callback=self.handle_badge_click
        )
        badge_item.set_badge(stackit.BadgeType.NEW_ITEMS, count=3)  # New enum approach
        self.app.add(badge_item)

        # SF Symbol rendering modes demo
        symbol_layout = stackit.vstack([
            stackit.label("SF Symbol Rendering Modes:", bold=True),
            stackit.hstack([
                stackit.image(stackit.SFSymbol(
                    "heart.fill",
                    rendering=stackit.SymbolRenderingMode.MONOCHROME,  # New enum
                    color="#FF3B30"
                )),
                stackit.image(stackit.SFSymbol(
                    "heart.fill",
                    rendering=stackit.SymbolRenderingMode.HIERARCHICAL,  # New enum
                    color="#FF3B30"
                )),
                stackit.image(stackit.SFSymbol(
                    "heart.fill",
                    rendering=stackit.SymbolRenderingMode.MULTICOLOR  # New enum
                )),
            ], alignment=stackit.Alignment.CENTER_Y, spacing=12.0),  # New enum
        ], spacing=8.0)

        symbol_item = stackit.MenuItem(layout=symbol_layout)
        self.app.add(symbol_item)

        # Radio group with new orientation enum
        radio_layout = stackit.vstack([
            stackit.label("Radio Group (Horizontal):", bold=True),
            stackit.radio_group(
                options=["Option A", "Option B", "Option C"],
                orientation=stackit.Orientation.HORIZONTAL,  # New enum approach
                selected=1,
                callback=self.handle_radio_change
            )
        ], spacing=8.0)

        radio_item = stackit.MenuItem(layout=radio_layout)
        self.app.add(radio_item)

        # Map view with new map type enum
        map_layout = stackit.vstack([
            stackit.label("Map View (Satellite):", bold=True),
            stackit.map_view(
                latitude=37.7749,
                longitude=-122.4194,
                dimensions=(300, 200),
                map_type=stackit.MapType.SATELLITE,  # New enum approach
                zoom=0.02
            )
        ], spacing=8.0)

        map_item = stackit.MenuItem(layout=map_layout)
        self.app.add(map_item)

        # Alignment demo
        alignment_layout = stackit.vstack([
            stackit.label("Alignment Demo:", bold=True),
            stackit.hstack([
                stackit.label("Leading"),
                stackit.spacer(),
                stackit.label("Trailing")
            ], alignment=stackit.Alignment.CENTER_Y),  # New enum approach
            stackit.hstack([
                stackit.button("Center X", callback=self.test_callback),
                stackit.button("Center Y", callback=self.test_callback),
            ], alignment=stackit.Alignment.CENTER_X),  # New enum approach
        ], spacing=8.0)

        alignment_item = stackit.MenuItem(layout=alignment_layout)
        self.app.add(alignment_item)

        # Configuration class demo
        self.add_config_demo()

        # Backward compatibility demo (with deprecation warnings)
        self.add_backward_compatibility_demo()

    def add_config_demo(self):
        """Demonstrate new configuration classes."""
        # Create SF Symbol using configuration class
        symbol_config = stackit.SFSymbolConfig(
            name="star.fill",
            rendering=stackit.SymbolRenderingMode.PALETTE,
            palette_colors=["#FFD700", "#FF6B35"],
            scale=stackit.SymbolScale.LARGE,
            weight=stackit.SymbolWeight.BOLD
        )

        # Note: This would be used in a future version that accepts config objects
        config_layout = stackit.vstack([
            stackit.label("Configuration Classes:", bold=True),
            stackit.label("• SFSymbolConfig for complex symbol setup"),
            stackit.label("• MapConfig for map view configuration"),
            stackit.label("• ChartConfig for chart customization"),
            stackit.label("(Demo: star symbol configured via dataclass)")
        ], spacing=4.0)

        config_item = stackit.MenuItem(layout=config_layout)
        self.app.add(config_item)

    def add_backward_compatibility_demo(self):
        """Demonstrate backward compatibility with string-based API."""
        compat_layout = stackit.vstack([
            stackit.label("Backward Compatibility:", bold=True),
            stackit.label("Old string API still works (with warnings):"),
            stackit.hstack([
                # This will work but show deprecation warnings
                stackit.image(stackit.SFSymbol(
                    "exclamationmark.triangle.fill",
                    rendering="hierarchical",  # Old string approach (deprecated)
                    color="#FF9500"
                )),
                stackit.label("Uses legacy string API")
            ], alignment="center_y", spacing=8.0),  # Old string approach (deprecated)
        ], spacing=6.0)

        compat_item = stackit.MenuItem(layout=compat_layout)
        self.app.add(compat_item)

    def handle_badge_click(self, sender):
        """Handle badge menu item click."""
        print("Badge item clicked - checking new features!")
        stackit.notification("Badge Demo", "New features checked!")

    def handle_radio_change(self, sender):
        """Handle radio button selection change."""
        print(f"Radio selection changed: {sender}")

    def test_callback(self, sender):
        """Test callback for buttons."""
        print(f"Button clicked: {sender}")

    def run(self):
        """Start the application."""
        print("Starting Enum Demo App...")
        print("This demo showcases:")
        print("• Type-safe enum-based API")
        print("• Backward compatibility with strings")
        print("• Configuration dataclasses")
        print("• Improved IDE support and autocompletion")
        print()
        self.app.run()


if __name__ == "__main__":
    app = EnumDemoApp()
    app.run()