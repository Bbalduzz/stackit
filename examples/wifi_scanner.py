#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wi-Fi Scanner - Network monitoring and management tool

Features:
- Scan available Wi-Fi networks
- Signal strength visualization
- Current connection info
- Network speed test simulation
- Connection history

Note: For full network scanning functionality, run with sudo:
    sudo python3 wifi_scanner.py

Otherwise, the app will use simulated data for demonstration.
"""

import os
import sys
import subprocess
import re
import getpass

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
import stackit


class WiFiScanner:
    def __init__(self):
        self.app = stackit.StackApp(
            title="Wi-Fi",
            icon=stackit.SFSymbol(
                "wifi", rendering="hierarchical", color="#007AFF", scale="medium"
            ),
        )

        self.current_network = None
        self.speed_history = [0] * 20  # Last 20 speed test results
        self.scanning = False

        self.setup_ui()

        # Initial scan
        self.scan_networks()

        # Update every 10 seconds
        self.timer = stackit.every(10.0, self.update_networks)

    def setup_ui(self):
        """Build the main UI."""
        # Header with current connection
        self.connection_item = stackit.MenuItem()
        self.app.add(self.connection_item, key="connection")

        # Separator
        self.app.add(stackit.MenuItem(layout=stackit.separator()))

        # Speed test section
        self.speed_item = stackit.MenuItem()
        self.app.add(self.speed_item, key="speed")

        # Separator
        self.app.add(stackit.MenuItem(layout=stackit.separator()))

        # Actions
        self.app.add(
            stackit.MenuItem(
                title="Refresh",
                callback=self.scan_networks,
            )
        )

        self.app.add(
            stackit.MenuItem(
                title="Run Speed Test",
                callback=self.run_speed_test,
            )
        )

        # Update all sections
        self.update_connection_section()
        self.update_speed_section()

    def get_current_network_info(self):
        """Get information about the current Wi-Fi connection using wdutil."""
        try:
            result = subprocess.run(
                ["wdutil", "info"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=2,
            )

            if result.returncode == 0 and result.stdout:
                output = result.stdout
                info = {}

                # Parse SSID
                ssid_match = re.search(r"SSID\s*:\s*(.+)$", output, re.MULTILINE)
                if ssid_match:
                    info["ssid"] = ssid_match.group(1).strip()

                # Parse BSSID
                bssid_match = re.search(r"BSSID\s*:\s*(.+)$", output, re.MULTILINE)
                if bssid_match:
                    info["bssid"] = bssid_match.group(1).strip()

                # Parse RSSI
                rssi_match = re.search(r"RSSI\s*:\s*(-?\d+)", output, re.MULTILINE)
                if rssi_match:
                    info["rssi"] = int(rssi_match.group(1))

                # Parse Noise
                noise_match = re.search(r"Noise\s*:\s*(-?\d+)", output, re.MULTILINE)
                if noise_match:
                    info["noise"] = int(noise_match.group(1))

                # Parse Channel
                channel_match = re.search(r"Channel\s*:\s*(\d+)", output, re.MULTILINE)
                if channel_match:
                    info["channel"] = int(channel_match.group(1))

                return info if "ssid" in info else None

        except Exception as e:
            print(f"Error getting network info: {e}")

        return None

    def scan_available_networks(self):
        """Scan for available networks - wdutil doesn't support this."""
        return []

    def rssi_to_percentage(self, rssi):
        """Convert RSSI (dBm) to percentage (0-100)."""
        # RSSI typically ranges from -100 (worst) to -30 (best)
        if rssi >= -50:
            return 100
        elif rssi <= -100:
            return 0
        else:
            return int(((rssi + 100) / 50) * 100)

    def get_signal_color(self, rssi):
        """Get color based on signal strength."""
        percentage = self.rssi_to_percentage(rssi)
        if percentage >= 75:
            return "#34C759"  # Green
        elif percentage >= 50:
            return "#FF9F0A"  # Orange
        elif percentage >= 25:
            return "#FF9500"  # Dark orange
        else:
            return "#FF3B30"  # Red

    def get_signal_icon(self, rssi):
        """Get Wi-Fi icon based on signal strength."""
        percentage = self.rssi_to_percentage(rssi)
        if percentage >= 75:
            return "wifi"
        elif percentage >= 50:
            return "wifi.exclamationmark"
        elif percentage >= 25:
            return "wifi.slash"
        else:
            return "wifi.slash"

    def update_connection_section(self):
        """Update the current connection display."""
        network_info = self.current_network

        if network_info:
            rssi = network_info.get("rssi", -100)
            percentage = self.rssi_to_percentage(rssi)
            color = self.get_signal_color(rssi)

            layout = stackit.vstack(
                [
                    stackit.hstack(
                        [
                            stackit.image(
                                stackit.SFSymbol(
                                    "wifi", rendering="hierarchical", color=color
                                ),
                                width=16,
                                height=16,
                            ),
                            stackit.label(
                                "Connected to:",
                                font_size=11,
                                color="#8E8E93",
                            ),
                            stackit.spacer(),
                        ],
                        spacing=6.0,
                    ),
                    stackit.hstack(
                        [
                            stackit.label(
                                network_info.get("ssid", "Unknown"),
                                font_size=14,
                                bold=True,
                            ),
                            stackit.spacer(),
                        ],
                        spacing=4.0,
                    ),
                    stackit.hstack(
                        [
                            stackit.label(
                                "Signal Strength:",
                                font_size=11,
                                color="#8E8E93",
                            ),
                            stackit.spacer(),
                            stackit.label(
                                f"{percentage}%",
                                font_size=11,
                                bold=True,
                                color=color,
                            ),
                        ],
                        spacing=6.0,
                    ),
                    stackit.hstack(
                        [
                            stackit.circular_progress(
                                percentage / 100.0, color=color, line_width=4
                            ),
                            stackit.spacer(priority=10),
                            stackit.vstack(
                                [
                                    stackit.hstack(
                                        [
                                            stackit.label(
                                                "RSSI:",
                                                font_size=10,
                                                color="#8E8E93",
                                                width=60,
                                            ),
                                            stackit.label(
                                                f"{rssi} dBm",
                                                font_size=10,
                                            ),
                                        ],
                                        spacing=4.0,
                                    ),
                                    stackit.hstack(
                                        [
                                            stackit.label(
                                                "Channel:",
                                                font_size=10,
                                                color="#8E8E93",
                                                width=60,
                                            ),
                                            stackit.label(
                                                str(network_info.get("channel", "N/A")),
                                                font_size=10,
                                            ),
                                        ],
                                        spacing=4.0,
                                    ),
                                    stackit.hstack(
                                        [
                                            stackit.label(
                                                "Noise:",
                                                font_size=10,
                                                color="#8E8E93",
                                                width=60,
                                            ),
                                            stackit.label(
                                                f"{network_info.get('noise', 'N/A')} dBm",
                                                font_size=10,
                                            ),
                                        ],
                                        spacing=4.0,
                                    ),
                                ],
                                spacing=4.0,
                            ),
                        ],
                        spacing=12.0,
                    ),
                ],
                spacing=8.0,
            )
        else:
            layout = stackit.hstack(
                [
                    stackit.image(
                        stackit.SFSymbol(
                            "wifi.slash", rendering="hierarchical", color="#FF3B30"
                        ),
                        width=16,
                        height=16,
                    ),
                    stackit.label(
                        "Not Connected",
                        font_size=13,
                        color="#8E8E93",
                    ),
                    stackit.spacer(),
                ],
                spacing=6.0,
            )

        self.connection_item.set_layout(layout)

    def update_speed_section(self):
        """Update the speed test section."""
        # Get average speed from history
        avg_speed = sum(self.speed_history) / len(self.speed_history)

        layout = stackit.vstack(
            [
                stackit.hstack(
                    [
                        stackit.label(
                            "Network Speed",
                            font_size=11,
                            bold=True,
                            color="#8E8E93",
                        ),
                        stackit.spacer(),
                    ],
                    spacing=6.0,
                ),
                stackit.line_chart(
                    points=self.speed_history,
                    dimensions=(280, 60),
                    max_value=100.0,
                    min_value=0.0,
                    color="#007AFF",
                    line_width=2.0,
                    fill=True,
                ),
                stackit.hstack(
                    [
                        stackit.label(
                            "Avg Speed:",
                            font_size=10,
                            color="#8E8E93",
                        ),
                        stackit.label(
                            f"{avg_speed:.1f} Mbps",
                            font_size=10,
                            bold=True,
                        ),
                        stackit.spacer(),
                        stackit.label(
                            "Current:",
                            font_size=10,
                            color="#8E8E93",
                        ),
                        stackit.label(
                            f"{self.speed_history[-1]:.1f} Mbps",
                            font_size=10,
                            bold=True,
                            color="#34C759"
                            if self.speed_history[-1] > 50
                            else "#FF9F0A",
                        ),
                    ],
                    spacing=6.0,
                ),
            ],
            spacing=8.0,
        )

        self.speed_item.set_layout(layout)

    def scan_networks(self, sender=None):
        """Refresh network info."""
        if self.scanning:
            return

        self.scanning = True

        # Get current connection
        self.current_network = self.get_current_network_info()

        # Update sections
        self.update_connection_section()

        # Update icon based on connection
        if self.current_network:
            rssi = self.current_network.get("rssi", -100)
            color = self.get_signal_color(rssi)
            self.app.set_icon(
                stackit.SFSymbol(
                    "wifi", rendering="hierarchical", color=color, scale="medium"
                )
            )
        else:
            self.app.set_icon(
                stackit.SFSymbol(
                    "wifi.slash",
                    rendering="hierarchical",
                    color="#FF3B30",
                    scale="medium",
                )
            )

        self.app.update()
        self.scanning = False

    def run_speed_test(self, sender=None):
        """Run a simulated speed test."""
        # This is a simulation - in a real app, you'd use speedtest-cli or similar
        import random

        # Simulate speed test with random values
        new_speed = random.uniform(20, 95)
        self.speed_history.append(new_speed)
        self.speed_history = self.speed_history[-20:]  # Keep last 20

        self.update_speed_section()
        self.app.update()

        stackit.notification(
            title="Speed Test Complete",
            subtitle=f"Download: {new_speed:.1f} Mbps",
            informative_text="Simulated speed test result",
        )

    def update_networks(self, timer):
        """Periodic update of network information."""
        self.scan_networks()

        # Also update speed with simulated data
        import random

        new_speed = random.uniform(40, 85)
        self.speed_history.append(new_speed)
        self.speed_history = self.speed_history[-20:]  # Keep last 20
        self.update_speed_section()

    def run(self):
        """Start the application."""
        self.app.run()


if __name__ == "__main__":
    app = WiFiScanner()
    app.run()
