import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import stackit
import time

class TimerApp:
    def __init__(self):
        self.app = stackit.StackApp("timer", icon=stackit.SFSymbol("timer", rendering="hierarchical", scale="medium"))
        self.start_time = time.time()
        self.setup_ui()

        # Update every second
        self.timer = stackit.every(1.0, self.update_display)

    def setup_ui(self):
        # Create timer display item (without layout initially)
        self.item = stackit.MenuItem()
        # reset button
        self.reset_item = stackit.MenuItem(
        	layout=stackit.hstack([
	            stackit.button("🔄 Reset Timer", target=self, action="reset_timer:")
	        ])
        )

        self.app.add(self.item)
        self.app.add(self.reset_item)
        self.app.add(
	        stackit.MenuItem(
		        title="Preferences...",
		        key_equivalent="p"  # ⌘,
		    )
        )
        self.update_display(None)

    def update_display(self, timer):
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60

        print(f"{minutes:02d}:{seconds:02d}")

        # Update layout dynamically
        layout = stackit.hstack([
            stackit.label("Time:", bold=True),
            stackit.spacer(),
            stackit.label(f"{minutes:02d}:{seconds:02d}", font_size=14)
        ], spacing=8)
        self.item.set_layout(layout)

        # Force the app to update the menu display
        self.app.update()

    def reset_timer_(self, sender):
        self.start_time = time.time()

    def run(self):
        self.app.run()

if __name__ == "__main__":
    TimerApp().run()