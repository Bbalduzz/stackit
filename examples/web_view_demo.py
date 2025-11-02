#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web View Demo - Demonstrates the web_view() control using WebKit

This example shows how to embed web content in a menu bar app
using both URLs and HTML strings.
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
        title="Web View", icon=stackit.SFSymbol("globe", color="#4A90E2")
    )

    # Example 1: Load a website
    website_view = stackit.web_view(
        url="https://netflix.com",
        private_mode=False,
        dimensions=(500, 400),
        enable_javascript=True,
        border_radius=12.0,
    )

    website_item = stackit.MenuItem(
        layout=stackit.vstack(
            [
                stackit.label("Website Example", bold=True, font_size=14),
                stackit.separator(),
                website_view,
                stackit.separator(),
                stackit.label("Loading example.com", font_size=10, color="gray"),
            ],
            spacing=8,
        )
    )

    app.add(website_item)

    # Example 2: Load custom HTML
    custom_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                margin: 0;
                padding: 20px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            h1 {
                font-size: 32px;
                margin: 0 0 10px 0;
                text-align: center;
            }
            p {
                font-size: 16px;
                opacity: 0.9;
                margin: 0 0 20px 0;
                text-align: center;
            }
            .counter {
                font-size: 48px;
                font-weight: bold;
                margin: 20px 0;
            }
            button {
                background: rgba(255,255,255,0.2);
                border: 2px solid white;
                color: white;
                padding: 12px 24px;
                font-size: 16px;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s;
            }
            button:hover {
                background: rgba(255,255,255,0.3);
                transform: scale(1.05);
            }
        </style>
    </head>
    <body>
        <h1>✨ StackIt Web View</h1>
        <p>Interactive HTML content with JavaScript</p>
        <div class="counter" id="counter">0</div>
        <button onclick="increment()">Click Me!</button>

        <script>
            let count = 0;
            function increment() {
                count++;
                document.getElementById('counter').textContent = count;
            }
        </script>
    </body>
    </html>
    """

    html_view = stackit.web_view(
        html=custom_html,
        dimensions=(500, 400),
        enable_javascript=True,
        border_radius=12.0,
    )

    html_item = stackit.MenuItem(
        layout=stackit.vstack(
            [
                stackit.label("Custom HTML Example", bold=True, font_size=14),
                stackit.separator(),
                html_view,
                stackit.separator(),
                stackit.label(
                    "Interactive HTML with JavaScript", font_size=10, color="gray"
                ),
            ],
            spacing=8,
        )
    )

    app.add(html_item)

    # Info item
    info_item = stackit.MenuItem(
        layout=stackit.vstack(
            [
                stackit.label("Web View Features:", bold=True),
                stackit.label("• Load any URL or custom HTML", font_size=11),
                stackit.label("• Full JavaScript support", font_size=11),
                stackit.label("• Transparent backgrounds", font_size=11),
                stackit.label("• Rounded corners support", font_size=11),
                stackit.label("• Powered by WebKit", font_size=11),
            ],
            spacing=4,
        )
    )

    app.add(info_item)

    # Run the app
    app.run()


if __name__ == "__main__":
    main()
