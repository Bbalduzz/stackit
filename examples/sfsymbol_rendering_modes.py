#!/usr/bin/env python3
"""
Demo showing SF Symbol rendering modes: monochrome, hierarchical, palette, and multicolor.
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import stackit


class SymbolRenderingDemo:
    def __init__(self):
        self.app = stackit.StackApp(title="SF Symbols", icon=stackit.SFSymbol("timer.circle", rendering="hierarchical", color="#ffffff", point_size=16))
        self.setup_ui()

    def create_symbol_row(self, title, symbol):
        """Create a row with title and symbol."""
        return stackit.hstack([
            stackit.label(title, font_size=12, bold=False),
            stackit.spacer(),
            stackit.image(symbol, width=24, height=24)
        ])

    def setup_ui(self):
        """Set up the UI layout."""
        content = stackit.vstack([
            stackit.label("Rendering Modes", bold=True, font_size=14),
            stackit.separator(),

            # Monochrome mode (single color)
            self.create_symbol_row(
                "Monochrome Red",
                stackit.SFSymbol("heart.fill", rendering="monochrome", color="#FF0000", point_size=20)
            ),

            # Hierarchical mode (base color with opacity variations)
            self.create_symbol_row(
                "Hierarchical Blue",
                stackit.SFSymbol("cloud.sun.fill", rendering="hierarchical", color="#0000FF", point_size=20)
            ),

            # Palette mode (multiple colors for different layers)
            self.create_symbol_row(
                "Palette RGB",
                stackit.SFSymbol("flag.fill", rendering="palette",
                                palette_colors=["#FF0000", "#00FF00", "#0000FF"], point_size=20)
            ),

            # Multicolor mode (uses symbol's built-in colors)
            self.create_symbol_row(
                "Multicolor",
                stackit.SFSymbol("rainbow", rendering="multicolor", point_size=20)
            ),

            stackit.separator(),

            # More examples
            stackit.label("More Examples", bold=True, font_size=14),
            stackit.separator(),

            self.create_symbol_row(
                "Battery (Hierarchical)",
                stackit.SFSymbol("battery.100.bolt", rendering="hierarchical", color="#ffffff", point_size=20)
            ),

            self.create_symbol_row(
                "Person (Palette)",
                stackit.SFSymbol("person.fill", rendering="palette",
                                palette_colors=["#FF9500", "#FFD60A"], point_size=20)
            ),

            self.create_symbol_row(
                "Wifi (Hierarchical)",
                stackit.SFSymbol("wifi", rendering="hierarchical", color="#007AFF", point_size=20)
            ),
        ], spacing=8)

        # Wrap in block
        block = stackit.block(
            content,
            radius=8.0,
            padding=16.0
        )

        item = stackit.MenuItem(layout=block)
        self.app.add(item)

    def run(self):
        """Run the application."""
        self.app.run()


if __name__ == "__main__":
    demo = SymbolRenderingDemo()
    demo.run()
