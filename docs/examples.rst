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
