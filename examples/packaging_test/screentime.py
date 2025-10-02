#!/usr/bin/env python3
"""
macOS Screen Time Tracker - Monitor app usage using StackIt

Reads from the macOS Knowledge database (knowledgeC.db) and displays
app usage statistics with beautiful line charts in the menu bar.

Requirements:
- macOS 10.15+ (Catalina or later)
- Full Disk Access permission for Terminal/Python
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import stackit
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

KNOWLEDGE_DB = os.path.expanduser("~/Library/Application Support/Knowledge/knowledgeC.db")

class ScreenTimeTracker:
    def __init__(self):
        # Create the app
        self.app = stackit.StackApp(
            icon=stackit.SFSymbol("chart.bar.xaxis.ascending.badge.clock", rendering="hierarchical")
        )

        # Check database access
        self.db_accessible = self.check_database_access()

        # Cache for app usage data
        self.app_usage = {}
        self.hourly_usage = []
        self.top_apps = []

        if self.db_accessible:
            self.load_screen_time_data()

    def check_database_access(self):
        """Check if we can access the Knowledge database."""
        if not os.path.exists(KNOWLEDGE_DB):
            print(f"❌ Could not find knowledgeC.db at {KNOWLEDGE_DB}")
            return False

        if not os.access(KNOWLEDGE_DB, os.R_OK):
            print(f"❌ The knowledgeC.db is not readable.")
            print("Please grant Full Disk Access to your terminal/Python:")
            print("  System Settings → Privacy & Security → Full Disk Access")
            return False

        print("✓ Database access granted")
        return True

    def query_screen_time(self, hours_back=24):
        """Query screen time data from the Knowledge database."""
        if not self.db_accessible:
            return []

        try:
            with sqlite3.connect(KNOWLEDGE_DB) as con:
                cur = con.cursor()

                # Calculate cutoff time (hours_back hours ago)
                cutoff_timestamp = datetime.now().timestamp() - (hours_back * 3600) - 978307200

                # Query app usage from the last N hours
                query = """
                SELECT
                    ZOBJECT.ZVALUESTRING AS app,
                    (ZOBJECT.ZENDDATE - ZOBJECT.ZSTARTDATE) AS usage_seconds,
                    (ZOBJECT.ZSTARTDATE + 978307200) as start_time,
                    (ZOBJECT.ZENDDATE + 978307200) as end_time
                FROM
                    ZOBJECT
                    LEFT JOIN ZSTRUCTUREDMETADATA
                        ON ZOBJECT.ZSTRUCTUREDMETADATA = ZSTRUCTUREDMETADATA.Z_PK
                WHERE
                    ZSTREAMNAME = "/app/usage"
                    AND ZOBJECT.ZSTARTDATE > ?
                    AND ZOBJECT.ZVALUESTRING IS NOT NULL
                ORDER BY
                    ZSTARTDATE DESC
                """

                cur.execute(query, (cutoff_timestamp,))
                return cur.fetchall()
        except Exception as e:
            print(f"Error querying database: {e}")
            return []

    def get_app_info(self, bundle_id):
        """Get the actual app icon and name from bundle identifier using NSWorkspace.

        Falls back to SF Symbol if app is not found.
        """
        import AppKit

        # Try to get the actual app icon
        workspace = AppKit.NSWorkspace.sharedWorkspace()
        app_url = workspace.URLForApplicationWithBundleIdentifier_(bundle_id)
        app_name = bundle_id.split('.')[-1].title()
        if app_url:
            # Get the app icon as NSImage
            icon = workspace.iconForFile_(app_url.path())
            bundle = AppKit.NSBundle.bundleWithPath_(app_url.path())
            if bundle:
                info = bundle.infoDictionary()
                if info and "CFBundleName" in info:
                    app_name = info["CFBundleName"]

            return icon, app_name

        # Default SF Symbol icon and app_name
        return stackit.SFSymbol('app', rendering="hierarchical", color="#4ECDC4"), app_name

    def load_screen_time_data(self):
        """Load and process screen time data."""
        rows = self.query_screen_time(hours_back=24)

        if not rows:
            return

        # Aggregate usage by app
        app_totals = defaultdict(float)
        hourly_data = defaultdict(float)  # Hour -> total minutes

        for row in rows:
            app_name = row[0]
            usage_seconds = row[1]
            start_time = datetime.fromtimestamp(row[2])

            # Skip very short usage (< 5 seconds, likely noise)
            if usage_seconds < 5:
                continue

            # Aggregate by app
            app_totals[app_name] += usage_seconds / 60  # Convert to minutes

            # Aggregate by hour
            hour_key = start_time.hour
            hourly_data[hour_key] += usage_seconds / 60

        # Get top 5 apps
        sorted_apps = sorted(app_totals.items(), key=lambda x: x[1], reverse=True)
        self.top_apps = sorted_apps[:5]
        self.app_usage = dict(app_totals)

        # Prepare hourly usage for chart (last 12 hours)
        current_hour = datetime.now().hour
        self.hourly_usage = []
        for i in range(12):
            hour = (current_hour - 11 + i) % 24
            minutes = hourly_data.get(hour, 0.0)
            self.hourly_usage.append(minutes)

        print(f"✓ Loaded data for {len(app_totals)} apps")
        print(f"✓ Total usage: {sum(app_totals.values()):.1f} minutes")

    def setup_menu(self):
        """Build the menu structure."""

        if not self.db_accessible:
            self.create_error_menu()
            return

        # ========== Today's Overview Block ==========
        total_minutes = sum(self.app_usage.values())
        total_hours = total_minutes / 60

        overview_block = stackit.block(
            stackit.vstack([
                stackit.label("Today's Screen Time", bold=True, color="#4ECDC4", font_size=14),
                stackit.hstack([
                    stackit.label(f"{total_hours:.1f}h", font_size=24, bold=True, color="#FF6B35"),
                    stackit.spacer(),
                    stackit.label(f"{len(self.app_usage)} apps", color="#888888")
                ])
            ], spacing=6.0),
            radius=8.0,
            # background_color="#1a1a1a"
        )

        overview_item = stackit.MenuItem(layout=overview_block)
        self.app.add(overview_item)

        # ========== Usage Chart Block ==========
        if self.hourly_usage:
            max_usage = max(self.hourly_usage) if self.hourly_usage else 60.0

            chart_block = stackit.block(
                stackit.vstack([
                    stackit.label("Last 12 Hours", bold=True, color="#95E1D3"),
                    stackit.line_chart(
                        points=self.hourly_usage,
                        dimensions=(280, 60),
                        max_value=max(max_usage, 10.0),  # At least 10 minutes scale
                        min_value=0.0,
                        # color="#4ECDC4",
                        line_width=2.0,
                        fill=True
                    ),
                    stackit.hstack([
                        stackit.label("0-60 min/hr", color="#888888", font_size=10),
                        stackit.spacer()
                    ])
                ], spacing=8.0),
                radius=8.0
            )

            chart_item = stackit.MenuItem(layout=chart_block)
            self.app.add(chart_item)


        # ========== Top Apps Block ==========
        if self.top_apps:
            top_apps_controls = [
                stackit.label("Top Apps", bold=True, color="#F38181")
            ]

            for i, (identifier, minutes) in enumerate(self.top_apps, 1):
                # Clean up app name (remove bundle identifier if present)
                # Get app icon (either real NSImage or SF Symbol fallback)
                icon, display_name = self.get_app_info(identifier)

                hours = minutes / 60
                time_str = f"{hours:.1f}h" if hours >= 1 else f"{int(minutes)}m"

                app_row = stackit.hstack([
                    stackit.image(icon, width=16, height=16),
                    stackit.label(display_name, bold=True),
                    stackit.spacer(),
                    stackit.label(time_str, color="#888888")
                ])

                top_apps_controls.append(app_row)

            top_apps_block = stackit.block(
                stackit.vstack(top_apps_controls, spacing=10.0),
                radius=8.0
            )

            top_apps_item = stackit.MenuItem(layout=top_apps_block)
            self.app.add(top_apps_item)

        self.app.add_separator()

        # ========== Actions ==========
        refresh_item = stackit.MenuItem(
            title="Refresh Data",
            callback=self.refresh_data,
            key_equivalent="r"
        )

        # Export submenu
        export_submenu = [
            stackit.MenuItem(title="Export as JSON", callback=self.export_json),
            stackit.MenuItem(title="Export as CSV", callback=self.export_csv)
        ]
        export_item = stackit.MenuItem(title="Export", submenu=export_submenu)
        self.app.add(export_item)
        self.app.add(refresh_item)

    def create_error_menu(self):
        """Create menu when database is not accessible."""
        error_block = stackit.block(
            stackit.vstack([
                stackit.image(stackit.SFSymbol("exclamationmark.triangle.fill",
                                               rendering="hierarchical",
                                               color="#FF6B35"),
                             width=40, height=40),
                stackit.label("Database Access Required", bold=True, font_size=14),
                stackit.label("Grant Full Disk Access to:", color="#888888", wraps=True, width=250),
                stackit.label("Terminal or Python", bold=True, color="#4ECDC4"),
                stackit.label("System Settings → Privacy & Security",
                            color="#888888", font_size=11, wraps=True, width=250)
            ], spacing=8.0),
            radius=8.0
        )

        error_item = stackit.MenuItem(layout=error_block)
        self.app.add(error_item)

        self.app.add_separator()

        help_item = stackit.MenuItem(
            title="How to Fix This...",
            callback=self.show_help
        )
        self.app.add(help_item)

    def refresh_data(self, sender):
        """Refresh screen time data."""
        print("Refreshing screen time data...")
        self.load_screen_time_data()

        # Rebuild menu
        # Clear all menu items from the menu directly
        menu = self.app._menu
        for item in list(menu.itemArray()):
            menu.removeItem_(item)

        # Clear the menu items dict
        self.app._menu_items.clear()

        # Reset the default items flag so Quit button gets re-added
        self.app._default_items_added = False

        # Rebuild the menu
        self.setup_menu()

        # Ensure default items (separator + Quit) are added back
        self.app._ensure_default_items()

        stackit.notification("Screen Time", "Data refreshed successfully!")

    def export_json(self, sender):
        """Export data as JSON."""
        import json

        data = {
            "timestamp": datetime.now().isoformat(),
            "total_minutes": sum(self.app_usage.values()),
            "apps": [
                {"name": app, "minutes": minutes}
                for app, minutes in sorted(self.app_usage.items(),
                                          key=lambda x: x[1],
                                          reverse=True)
            ]
        }

        # Save to desktop
        desktop = os.path.expanduser("~/Downloads")
        filename = os.path.join(desktop, f"screentime_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Exported to: {filename}")
        stackit.notification("Export Complete", f"Saved to Downloads")

    def export_csv(self, sender):
        """Export data as CSV."""
        import csv

        desktop = os.path.expanduser("~/Downloads")
        filename = os.path.join(desktop, f"screentime_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["App", "Minutes", "Hours"])

            for app, minutes in sorted(self.app_usage.items(),
                                       key=lambda x: x[1],
                                       reverse=True):
                writer.writerow([app, f"{minutes:.2f}", f"{minutes/60:.2f}"])

        print(f"Exported to: {filename}")
        stackit.notification("Export Complete", f"Saved to Downloads")

    def show_help(self, sender):
        """Show help dialog."""
        stackit.alert(
            "Full Disk Access Required",
            "To track screen time, this app needs Full Disk Access.\n\n"
            "Steps:\n"
            "1. Open System Settings\n"
            "2. Go to Privacy & Security → Full Disk Access\n"
            "3. Enable access for Terminal (or your Python app)\n"
            "4. Restart this app\n\n"
            "This allows reading from:\n"
            "~/Library/Application Support/Knowledge/knowledgeC.db",
            ok="Got it"
        )

    def auto_refresh(self, timer):
        """Auto-refresh data every minute."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Auto-refreshing screen time data...")

        # Store current scroll position or state if needed
        old_total = sum(self.app_usage.values()) if self.app_usage else 0

        # Reload data
        self.load_screen_time_data()

        # Rebuild menu
        menu = self.app._menu
        for item in list(menu.itemArray()):
            menu.removeItem_(item)

        self.app._menu_items.clear()
        self.app._default_items_added = False

        self.setup_menu()
        self.app._ensure_default_items()

        # Log changes
        new_total = sum(self.app_usage.values()) if self.app_usage else 0
        if new_total != old_total:
            delta = new_total - old_total
            print(f"  Updated: +{delta:.1f} minutes of usage")

    def run(self):
        """Start the application."""
        self.setup_menu()

        print("\n" + "="*60)
        print("macOS Screen Time Tracker")
        print("="*60)

        if self.db_accessible:
            print(f"✓ Tracking {len(self.app_usage)} apps")
            print(f"✓ Total usage: {sum(self.app_usage.values())/60:.1f} hours")
            print(f"✓ Auto-refresh: Every 60 seconds")
            print("\nPress ⌘R to refresh manually")

            # Start auto-refresh timer (every 60 seconds)
            stackit.every(60.0, self.auto_refresh)
        else:
            print("⚠️  Database not accessible - see menu for instructions")

        print("="*60 + "\n")

        self.app.run()

if __name__ == "__main__":
    tracker = ScreenTimeTracker()
    tracker.run()
