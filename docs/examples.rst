Examples
========

Complete Examples
-----------------

Timer Application
~~~~~~~~~~~~~~~~~

A menu bar app that shows elapsed time::

    import rumps
    import time

    class TimerApp(rumps.App):
        def __init__(self):
            super(TimerApp, self).__init__("Timer")
            self.start_time = time.time()
            self.timer = rumps.Timer(self.update_title, 1)
            self.timer.start()

        def update_title(self, _):
            elapsed = int(time.time() - self.start_time)
            self.title = f"⏱ {elapsed}s"

        @rumps.clicked("Reset")
        def reset(self, _):
            self.start_time = time.time()

    if __name__ == "__main__":
        TimerApp().run()

Network Status Monitor
~~~~~~~~~~~~~~~~~~~~~~

Monitor network connectivity::

    import rumps
    import subprocess

    class NetworkMonitor(rumps.App):
        def __init__(self):
            super().__init__("Net")
            self.icon = rumps.Icon(sf_symbol="wifi")
            self.menu = ["Check Status"]
            self.timer = rumps.Timer(self.check_network, 30)
            self.timer.start()

        def check_network(self, _):
            try:
                subprocess.check_call(
                    ["ping", "-c", "1", "8.8.8.8"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.icon = rumps.Icon(sf_symbol="wifi")
            except subprocess.CalledProcessError:
                self.icon = rumps.Icon(sf_symbol="wifi.slash")

        @rumps.clicked("Check Status")
        def manual_check(self, _):
            self.check_network(None)
            rumps.notification(
                "Network Status",
                "Check Complete",
                "Network status updated"
            )

    if __name__ == "__main__":
        NetworkMonitor().run()

Todo List
~~~~~~~~~

A simple todo list in the menu bar::

    import rumps

    class TodoApp(rumps.App):
        def __init__(self):
            super().__init__("📝")
            self.todos = []
            self.menu = ["Add Todo", None]  # None creates a separator

        @rumps.clicked("Add Todo")
        def add_todo(self, _):
            response = rumps.Window(
                "Add a todo item",
                "Enter your todo:",
                dimensions=(200, 20)
            ).run()

            if response.clicked:
                todo = response.text
                if todo:
                    self.todos.append(todo)
                    item = rumps.MenuItem(
                        todo,
                        callback=self.toggle_todo
                    )
                    self.menu.add(item)

        def toggle_todo(self, sender):
            sender.state = not sender.state
            if sender.state:
                sender.title = f"✓ {sender.title}"
            else:
                sender.title = sender.title.replace("✓ ", "")

    if __name__ == "__main__":
        TodoApp().run()

System Information
~~~~~~~~~~~~~~~~~~

Display system information in the menu bar::

    import rumps
    import psutil

    class SystemInfo(rumps.App):
        def __init__(self):
            super().__init__("💻")
            self.timer = rumps.Timer(self.update_info, 5)
            self.timer.start()
            self.update_info(None)

        def update_info(self, _):
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent

            self.menu.clear()
            self.menu.add(rumps.MenuItem(f"CPU: {cpu}%", callback=None))
            self.menu.add(rumps.MenuItem(f"Memory: {memory}%", callback=None))
            self.menu.add(None)  # Separator
            self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))

    if __name__ == "__main__":
        SystemInfo().run()
