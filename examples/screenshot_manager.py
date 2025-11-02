#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Screenshot Manager - Capture, manage and share screenshots

Features:
- Interactive window selection
- Recent screenshots gallery
- Quick actions (copy, delete, open)
- Auto-cleanup old screenshots
"""

import os
import sys
import subprocess
import time
import threading
from datetime import datetime
from pathlib import Path

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
import stackit


class ScreenshotManager:
    def __init__(self):
        self.app = stackit.StackApp(
            icon=stackit.SFSymbol(
                "camera.viewfinder",
                rendering="hierarchical",
                scale="medium",
            ),
        )

        # Create screenshots directory
        self.screenshots_dir = Path.home() / "Pictures" / "StackIt Screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)

        self.recent_screenshots = []
        self.max_recent = 3

        self.load_recent_screenshots()
        self.setup_ui()

    def setup_ui(self):
        """Build the main UI."""
        # Recent screenshots section
        self.recent_item = stackit.MenuItem()
        self.app.add(self.recent_item, key="recent")

        # Separator
        self.app.add(stackit.MenuItem(layout=stackit.separator()))

        # Actions
        self.app.add(
            stackit.MenuItem(
                title="Capture Window", callback=self.capture_window, key_equivalent="w"
            )
        )

        self.app.add(
            stackit.MenuItem(
                title="Capture Selection",
                callback=self.capture_selection,
                key_equivalent="s",
            )
        )

        self.app.add(
            stackit.MenuItem(
                title="Capture Full Screen",
                callback=self.capture_fullscreen,
                key_equivalent="f",
            )
        )

        # Separator
        self.app.add(stackit.MenuItem(layout=stackit.separator()))

        self.app.add(
            stackit.MenuItem(
                title="Open Screenshots Folder",
                callback=self.open_folder,
            )
        )

        # Update UI
        self.update_recent_section()

    def load_recent_screenshots(self):
        """Load recent screenshots from directory."""
        try:
            screenshots = list(self.screenshots_dir.glob("*.png"))
            screenshots.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            print(screenshots)
            self.recent_screenshots = screenshots[: self.max_recent]
        except Exception as e:
            print(f"Error loading screenshots: {e}")
            self.recent_screenshots = []

    def _update_ui_after_capture(self, filename, subtitle):
        """Update UI after screenshot capture (called on main thread)."""
        self.load_recent_screenshots()
        self.update_recent_section()
        self.app.update()

        stackit.notification(
            title="Screenshot Captured",
            message=subtitle,
            # informative_text=str(filename.name),
        )

    def capture_window(self, sender=None):
        """Capture a selected window."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = self.screenshots_dir / f"window_{timestamp}.png"

        def capture_thread():
            try:
                # -w: window mode (interactive selection)
                # -o: don't add shadow
                subprocess.run(
                    ["screencapture", "-w", str(filename)],
                    check=True,
                )

                if filename.exists():
                    stackit.after(
                        0.0,
                        lambda timer, f=filename, s="Window screenshot saved": self._update_ui_after_capture(
                            f, s
                        ),
                    )
            except subprocess.CalledProcessError:
                # User cancelled
                pass
            except Exception as e:
                print(f"Error capturing window: {e}")

        # Run capture in background thread to avoid blocking
        threading.Thread(target=capture_thread, daemon=True).start()

    def capture_selection(self, sender=None):
        """Capture a selected area."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = self.screenshots_dir / f"selection_{timestamp}.png"

        def capture_thread():
            try:
                # -s: selection mode (interactive)
                subprocess.run(
                    ["screencapture", "-s", str(filename)],
                    check=True,
                )

                # Check if file was created
                if filename.exists():
                    # stackit.after() is now thread-safe and can be called from background threads!
                    stackit.after(
                        0.0,
                        lambda timer, f=filename, s="Selection screenshot saved": self._update_ui_after_capture(
                            f, s
                        ),
                    )
            except subprocess.CalledProcessError:
                # User cancelled
                pass
            except Exception as e:
                print(f"Error capturing selection: {e}")

        # Run capture in background thread to avoid blocking
        threading.Thread(target=capture_thread, daemon=True).start()

    def capture_fullscreen(self, sender=None):
        """Capture full screen."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = self.screenshots_dir / f"fullscreen_{timestamp}.png"

        def capture_thread():
            try:
                # -x: no sound
                subprocess.run(
                    ["screencapture", "-x", str(filename)],
                    check=True,
                )

                # Schedule UI updates on main thread
                # stackit.after() is now thread-safe and can be called from background threads!
                stackit.after(
                    0.0,
                    lambda timer, f=filename, s="Full screen screenshot saved": self._update_ui_after_capture(
                        f, s
                    ),
                )
            except Exception as e:
                print(f"Error capturing fullscreen: {e}")

        # Run capture in background thread to avoid blocking
        threading.Thread(target=capture_thread, daemon=True).start()

    def open_folder(self, sender=None):
        """Open screenshots folder in Finder."""
        subprocess.run(["open", str(self.screenshots_dir)])

    def get_file_size_str(self, filepath):
        """Get human-readable file size."""
        size_bytes = filepath.stat().st_size
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

    def get_time_ago(self, filepath):
        """Get human-readable time since capture."""
        mtime = filepath.stat().st_mtime
        now = time.time()
        diff = now - mtime

        if diff < 60:
            return "Just now"
        elif diff < 3600:
            mins = int(diff / 60)
            return f"{mins}m ago"
        elif diff < 86400:
            hours = int(diff / 3600)
            return f"{hours}h ago"
        else:
            days = int(diff / 86400)
            return f"{days}d ago"

    def update_recent_section(self):
        """Update the recent screenshots display."""
        print("this is called")
        if not self.recent_screenshots:
            print(len(self.recent_screenshots))

            layout = stackit.block(
                stackit.hstack(
                    [
                        stackit.image(
                            stackit.SFSymbol(
                                "nosign.app.fill",
                                rendering=stackit.SymbolRenderingMode.HIERARCHICAL,
                            )
                        ),
                        stackit.label(
                            "No recent screenshots",
                            font_size=12,
                            color="#8E8E93",
                        ),
                        stackit.spacer(),
                    ],
                )
            )
        else:
            items = []

            for screenshot in self.recent_screenshots:
                # Screenshot info row
                info_row = stackit.hstack(
                    [
                        stackit.vstack(
                            [
                                stackit.label(
                                    screenshot.name[:30]
                                    + ("..." if len(screenshot.name) > 30 else ""),
                                    font_size=11,
                                    bold=True,
                                ),
                                stackit.hstack(
                                    [
                                        stackit.label(
                                            self.get_time_ago(screenshot),
                                            font_size=10,
                                            color="#8E8E93",
                                        ),
                                        stackit.label(
                                            "•", font_size=10, color="#8E8E93"
                                        ),
                                        stackit.label(
                                            self.get_file_size_str(screenshot),
                                            font_size=10,
                                            color="#8E8E93",
                                        ),
                                    ],
                                    spacing=4.0,
                                ),
                            ],
                            spacing=2.0,
                        ),
                        stackit.spacer(),
                    ],
                    spacing=8.0,
                )
                screenshot_group = stackit.block(
                    stackit.vstack(
                        [info_row],
                        spacing=6.0,
                    )
                )

                items.append(screenshot_group)

            layout = stackit.vstack(items, spacing=8.0)

        self.recent_item.set_layout(layout)

    def run(self):
        """Start the application."""
        self.app.run()


if __name__ == "__main__":
    app = ScreenshotManager()
    app.run()
