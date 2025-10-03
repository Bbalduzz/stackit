Examples
========

Complete Examples
-----------------

Timer Application
~~~~~~~~~~~~~~~~~

A menu bar app that shows elapsed time with a rich layout::

    import stackit
    import time

    class TimerApp:
        def __init__(self):
            self.app = stackit.StackApp("Timer", "⏱")
            self.start_time = time.time()
            self.setup_ui()

            # Update every second
            self.timer = stackit.every(1.0, self.update_display)

        def setup_ui(self):
            # Create timer display item (without layout initially)
            self.item = stackit.MenuItem()
            self.update_display(None)
            self.app.add(self.item)

            # Add reset button
            reset_layout = stackit.hstack([
                stackit.button("🔄 Reset Timer", target=self, action="reset_timer:")
            ])
            reset_item = stackit.MenuItem(layout=reset_layout)
            self.app.add(reset_item)

        def update_display(self, timer):
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60

            # Update layout dynamically
            layout = stackit.hstack([
                stackit.label("Time:", bold=True),
                stackit.spacer(),
                stackit.label(f"{minutes:02d}:{seconds:02d}", font_size=14)
            ], spacing=8)
            self.item.set_layout(layout)

            # Force menu to redraw
            self.app.update()

        def reset_timer_(self, sender):
            self.start_time = time.time()

        def run(self):
            self.app.run()

    if __name__ == "__main__":
        TimerApp().run()

Network Status Monitor
~~~~~~~~~~~~~~~~~~~~~~

Monitor network connectivity with visual indicators::

    import stackit
    import subprocess

    class NetworkMonitor:
        def __init__(self):
            self.app = stackit.StackApp("Net")
            self.connected = True
            self.setup_ui()

            # Check every 30 seconds
            self.timer = stackit.every(30.0, self.check_network)
            self.check_network(None)

        def setup_ui(self):
            # Status display (dynamic updates)
            self.status_item = stackit.MenuItem()
            self.app.add(self.status_item)

            self.app.add_separator()

            # Manual check button
            check_layout = stackit.hstack([
                stackit.button("🔄 Check Now", target=self, action="manual_check:")
            ])
            check_item = stackit.MenuItem(layout=check_layout)
            self.app.add(check_item)

        def check_network(self, timer):
            try:
                subprocess.check_call(
                    ["ping", "-c", "1", "8.8.8.8"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=5
                )
                self.connected = True
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                self.connected = False

            self.update_display()

        def update_display(self):
            if self.connected:
                icon = stackit.image(
                    stackit.SFSymbol("wifi", point_size=16, color="green"),
                    width=16, height=16
                )
                status_text = "Connected"
                color = "green"
            else:
                icon = stackit.image(
                    stackit.SFSymbol("wifi.slash", point_size=16, color="red"),
                    width=16, height=16
                )
                status_text = "Disconnected"
                color = "red"

            # Update layout
            layout = stackit.hstack([
                icon,
                stackit.label(status_text, color=color)
            ], spacing=8)
            self.status_item.set_layout(layout)

            # Update app icon
            app_icon = stackit.SFSymbol(
                "wifi" if self.connected else "wifi.slash",
                point_size=16
            )
            self.app.set_icon(app_icon)

            # Force menu to redraw
            self.app.update()

        def manual_check_(self, sender):
            self.check_network(None)
            stackit.notification(
                "Network Status",
                "Check Complete",
                f"Status: {'Connected' if self.connected else 'Disconnected'}"
            )

        def run(self):
            self.app.run()

    if __name__ == "__main__":
        NetworkMonitor().run()

Todo List Manager
~~~~~~~~~~~~~~~~~

A feature-rich todo list with checkboxes::

    import stackit

    class TodoApp:
        def __init__(self):
            self.app = stackit.StackApp("📝 Todos")
            self.todos = []
            self.setup_ui()

        def setup_ui(self):
            # Add todo button
            add_item = stackit.StackMenuItem("Add")
            layout = add_item.hstack()
            layout.append(stackit.button("➕ Add Todo", target=self, action="add_todo:"))
            add_item.set_root_stack(layout)
            self.app.add_item("add", add_item)

            self.app.add_separator()

        def add_todo_(self, sender):
            # Use alert as input dialog
            result = stackit.alert(
                "New Todo",
                "Enter your todo item:",
                ok="Add",
                cancel="Cancel"
            )

            if result == 1:  # OK clicked
                # In real app, you'd get text from a proper input dialog
                todo_text = f"Todo Item {len(self.todos) + 1}"
                self.add_todo_item(todo_text)

        def add_todo_item(self, text):
            todo_id = f"todo_{len(self.todos)}"
            self.todos.append({"id": todo_id, "text": text, "done": False})

            # Create todo item with checkbox
            item = stackit.StackMenuItem(todo_id)
            layout = item.hstack(spacing=8)

            checkbox = stackit.checkbox("", state=False)
            layout.append(checkbox)
            layout.append(stackit.label(text))

            item.set_root_stack(layout)
            self.app.add_item(todo_id, item)

        def run(self):
            self.app.run()

    if __name__ == "__main__":
        TodoApp().run()

System Monitor Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~

Display system information with progress bars::

    import stackit
    import psutil
    import platform

    class SystemMonitor:
        def __init__(self):
            self.app = stackit.StackApp("💻 System")
            self.setup_ui()

            # Update every 3 seconds
            self.timer = stackit.every(3.0, self.update_info)
            self.update_info(None)

        def setup_ui(self):
            # System info header
            info_item = stackit.StackMenuItem("Info")
            layout = info_item.vstack(spacing=4)
            layout.append(stackit.label(f"macOS {platform.mac_ver()[0]}", font_size=11, color="gray"))
            info_item.set_root_stack(layout)
            self.app.add_item("info", info_item)

            self.app.add_separator()

            # CPU display
            self.cpu_item = stackit.StackMenuItem("CPU")
            self.app.add_item("cpu", self.cpu_item)

            # Memory display
            self.mem_item = stackit.StackMenuItem("Memory")
            self.app.add_item("memory", self.mem_item)

            # Disk display
            self.disk_item = stackit.StackMenuItem("Disk")
            self.app.add_item("disk", self.disk_item)

        def update_info(self, timer):
            # Update CPU
            cpu_percent = psutil.cpu_percent(interval=1) / 100.0
            layout = self.cpu_item.vstack(spacing=4)
            layout.append(stackit.label("CPU Usage", font_size=11, bold=True))
            layout.append(stackit.progress_bar(width=200, value=cpu_percent))
            layout.append(stackit.label(f"{cpu_percent*100:.1f}%", font_size=10, color="gray"))
            self.cpu_item.set_root_stack(layout)

            # Update Memory
            mem = psutil.virtual_memory()
            mem_percent = mem.percent / 100.0
            layout = self.mem_item.vstack(spacing=4)
            layout.append(stackit.label("Memory Usage", font_size=11, bold=True))
            layout.append(stackit.progress_bar(width=200, value=mem_percent))
            layout.append(stackit.label(
                f"{mem.used / (1024**3):.1f} GB / {mem.total / (1024**3):.1f} GB",
                font_size=10,
                color="gray"
            ))
            self.mem_item.set_root_stack(layout)

            # Update Disk
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent / 100.0
            layout = self.disk_item.vstack(spacing=4)
            layout.append(stackit.label("Disk Usage", font_size=11, bold=True))
            layout.append(stackit.progress_bar(width=200, value=disk_percent))
            layout.append(stackit.label(
                f"{disk.used / (1024**3):.1f} GB / {disk.total / (1024**3):.1f} GB",
                font_size=10,
                color="gray"
            ))
            self.disk_item.set_root_stack(layout)

        def run(self):
            self.app.run()

    if __name__ == "__main__":
        SystemMonitor().run()

Music Player Controller
~~~~~~~~~~~~~~~~~~~~~~~

A compact music player controller with buttons and sliders::

    import stackit

    class MusicController:
        def __init__(self):
            self.app = stackit.StackApp("🎵")
            self.playing = False
            self.volume = 50
            self.setup_ui()

        def setup_ui(self):
            # Playback controls
            controls_item = stackit.StackMenuItem("Controls")
            layout = controls_item.hstack(spacing=8)

            # Previous button
            prev_btn = stackit.button("⏮", target=self, action="previous:")
            layout.append(prev_btn)

            # Play/Pause button
            self.play_btn = stackit.button("▶️", target=self, action="toggle_play:")
            layout.append(self.play_btn)

            # Next button
            next_btn = stackit.button("⏭", target=self, action="next:")
            layout.append(next_btn)

            controls_item.set_root_stack(layout)
            self.app.add_item("controls", controls_item)

            # Volume control
            volume_item = stackit.StackMenuItem("Volume")
            layout = volume_item.vstack(spacing=4)
            layout.append(stackit.label("Volume", font_size=11, bold=True))
            vol_slider = stackit.slider(width=150, min_value=0, max_value=100, value=self.volume)
            layout.append(vol_slider)
            volume_item.set_root_stack(layout)
            self.app.add_item("volume", volume_item)

        def toggle_play_(self, sender):
            self.playing = not self.playing
            # Update button would require accessing the control
            stackit.notification("Music", "", "▶️ Playing" if self.playing else "⏸ Paused")

        def previous_(self, sender):
            stackit.notification("Music", "", "⏮ Previous Track")

        def next_(self, sender):
            stackit.notification("Music", "", "⏭ Next Track")

        def run(self):
            self.app.run()

    if __name__ == "__main__":
        MusicController().run()

Video Player
~~~~~~~~~~~~

A menu bar app with embedded video player using AVKit::

    import stackit

    class VideoPlayerApp:
        def __init__(self):
            self.app = stackit.StackApp(
                title="Video",
                icon=stackit.SFSymbol("play.rectangle.fill", color="#FF6B6B")
            )
            self.setup_ui()

        def setup_ui(self):
            # Video player with controls
            video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

            video_player = stackit.video(
                video_url,
                dimensions=(400, 225),
                border_radius=12.0,
                show_controls=True,
                autoplay=False,
                loop=False
            )

            video_item = stackit.MenuItem(
                layout=stackit.vstack([
                    stackit.label("Video Player", bold=True, font_size=14),
                    stackit.separator(),
                    video_player,
                    stackit.separator(),
                    stackit.label("Sample video", font_size=10, color="gray"),
                ], spacing=8)
            )

            self.app.add(video_item)

        def run(self):
            self.app.run()

    if __name__ == "__main__":
        VideoPlayerApp().run()

Web Browser
~~~~~~~~~~~

A menu bar app with embedded web view using WebKit::

    import stackit

    class WebBrowserApp:
        def __init__(self):
            self.app = stackit.StackApp(
                title="Browser",
                icon=stackit.SFSymbol("safari.fill", color="#0080FF")
            )
            self.setup_ui()

        def setup_ui(self):
            # Web view with URL
            web = stackit.web_view(
                "https://news.ycombinator.com",
                dimensions=(600, 500),
                border_radius=12.0
            )

            web_item = stackit.MenuItem(
                layout=stackit.vstack([
                    stackit.label("Hacker News", bold=True, font_size=14),
                    stackit.separator(),
                    web,
                ], spacing=8)
            )

            self.app.add(web_item)

            # Custom HTML content
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: -apple-system; padding: 20px; }
                    h1 { color: #0080FF; }
                </style>
            </head>
            <body>
                <h1>Welcome</h1>
                <p>This is custom HTML content in your menu bar!</p>
            </body>
            </html>
            """

            custom_web = stackit.web_view(
                html_content,
                dimensions=(400, 200),
                border_radius=8.0
            )

            custom_item = stackit.MenuItem(
                layout=stackit.vstack([
                    stackit.label("Custom HTML", bold=True, font_size=14),
                    stackit.separator(),
                    custom_web,
                ], spacing=8)
            )

            self.app.add(custom_item)

        def run(self):
            self.app.run()

    if __name__ == "__main__":
        WebBrowserApp().run()

Map Viewer
~~~~~~~~~~

An interactive map viewer with annotations using MapKit::

    import stackit

    class MapViewerApp:
        def __init__(self):
            self.app = stackit.StackApp(
                title="Maps",
                icon=stackit.SFSymbol("map.fill", color="#4A90E2")
            )
            self.setup_ui()

        def setup_ui(self):
            # San Francisco map with annotations
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
                    stackit.label("Interactive map with pins", font_size=10, color="gray"),
                ], spacing=8)
            )

            self.app.add(sf_item)

            # New York - Satellite view
            ny_map = stackit.map_view(
                latitude=40.7128,
                longitude=-74.0060,
                zoom=0.03,
                dimensions=(400, 300),
                map_type="satellite",
                show_controls=True,
                border_radius=12.0
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

            self.app.add(ny_item)

        def run(self):
            self.app.run()

    if __name__ == "__main__":
        MapViewerApp().run()

Activity Rings Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~

Display fitness-style activity rings using ring charts::

    import stackit

    class ActivityDashboard:
        def __init__(self):
            self.app = stackit.StackApp(
                title="Activity",
                icon=stackit.SFSymbol("figure.run", color="#32D74B")
            )
            self.setup_ui()

            # Update every 5 seconds with new data
            self.timer = stackit.every(5.0, self.update_activity)

        def setup_ui(self):
            # Main activity rings
            main_rings = stackit.ring_chart(
                data=[85, 65, 45],
                dimensions=(120, 120),
                colors=["#32D74B", "#0A84FF", "#FF375F"],
                ring_width=12.0,
                spacing=3.0,
                labels=["Move", "Exercise", "Stand"]
            )

            main_item = stackit.MenuItem(
                layout=stackit.vstack([
                    stackit.label("Today's Activity", bold=True, font_size=14),
                    stackit.separator(),
                    main_rings,
                    stackit.separator(),
                    stackit.label("Move: 85% | Exercise: 65% | Stand: 45%",
                                  font_size=10, color="gray"),
                ], spacing=8)
            )
            self.app.add(main_item)

            # Weekly summary rings
            self.weekly_item = stackit.MenuItem()
            self.app.add(self.weekly_item)
            self.update_weekly()

        def update_weekly(self):
            # Show smaller rings for the week
            weekly_rings = stackit.ring_chart(
                data=[90, 75, 60, 85],
                dimensions=(80, 80),
                colors=["#FFD60A", "#FF9F0A", "#FF453A", "#BF5AF2"],
                ring_width=8.0,
                spacing=2.0
            )

            layout = stackit.vstack([
                stackit.label("Weekly Progress", bold=True, font_size=12),
                stackit.separator(),
                stackit.hstack([
                    stackit.label("Week:", font_size=10),
                    stackit.spacer(),
                    weekly_rings,
                ], spacing=8),
            ], spacing=6)

            self.weekly_item.set_layout(layout)

        def update_activity(self, timer):
            # In a real app, this would fetch actual activity data
            import random

            # Update main rings with new random values
            new_data = [
                random.randint(60, 100),
                random.randint(50, 90),
                random.randint(40, 80)
            ]

            # Force menu to update (would need to recreate the layout)
            self.app.update()

        def run(self):
            self.app.run()

    if __name__ == "__main__":
        ActivityDashboard().run()
