# StackIt 🚀

**A modern, powerful framework for creating beautiful macOS menu bar applications with rich custom layouts**

StackIt provides an elegant Python API for building native macOS status bar apps with SwiftUI-inspired layout patterns (hstack/vstack), extensive UI controls, and full SF Symbols support—all built directly on AppKit with zero external dependencies.

<p align="center">
  <img src="https://img.shields.io/badge/macOS-11.0+-blue.svg" alt="macOS 11.0+">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
</p>

---

## ✨ Key Features

- **🎨 Rich Layouts** - SwiftUI-inspired hstack/vstack for flexible, declarative layouts
- **🎛️ Extensive Controls** - Labels, buttons, sliders, progress bars, text fields, checkboxes, date pickers, and more
- **🔣 SF Symbols** - Full support for Apple's SF Symbols with customization (size, weight, color, rendering modes)
- **⚡ Native Performance** - Built directly on AppKit using PyObjC, no middleman libraries
- **🪶 Lightweight** - Minimal dependencies (just PyObjC), fully isolated framework
- **🔄 Dynamic Updates** - Real-time UI updates with timers and callbacks
- **💾 Preferences** - Built-in preference storage and retrieval
- **🔔 Notifications** - System notification support
- **📱 Modern API** - Clean, intuitive, Pythonic interface

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/yourusername/stackit.git
cd stackit
pip install -e .
```

Or simply copy the `stackit` directory into your project.

**Requirements:**
- macOS 11.0+ (for SF Symbols)
- Python 3.7+
- PyObjC (usually pre-installed on macOS)

### Hello World

```python
import stackit

# Create app
app = stackit.StackApp("Hello", "👋")

# Create a menu item with custom layout
item = stackit.StackMenuItem("Greeting")
layout = item.hstack()
layout.append(stackit.label("Hello, World!", bold=True))
item.set_root_stack(layout)

app.add_item("greeting", item)
app.run()
```

### Rich Layout Example

```python
import stackit

app = stackit.StackApp("Status", "📊")

# Create rich dashboard layout
item = stackit.StackMenuItem("Dashboard")
layout = item.vstack(spacing=8)

# Header with icon
header = item.hstack()
header.append(stackit.image(
    stackit.SFSymbol.create("chart.bar.fill", size=16, color="blue"),
    width=16, height=16
))
header.append(stackit.label("System Status", bold=True))
layout.append(header)

# Progress indicator
layout.append(stackit.label("Loading...", font_size=11, color="gray"))
layout.append(stackit.progress_bar(width=200, value=0.75))

# Action button
btn_row = item.hstack()
btn_row.append(stackit.spacer())
btn_row.append(stackit.button("Refresh", target=app, action="refresh:"))
layout.append(btn_row)

item.set_root_stack(layout)
app.add_item("dashboard", item)
app.run()
```

---

## 📚 Core Concepts

### 1. StackApp - Your Application

The main application class that manages your menu bar presence:

```python
app = stackit.StackApp(title="My App", icon="🎯")

# Add menu items
app.add_item("key", stack_menu_item)
app.add_separator()

# Manage appearance
app.set_title("New Title")
app.set_icon(stackit.SFSymbol.create("star.fill"))

# Run event loop
app.run()
```

### 2. StackMenuItem - Menu Items

Individual menu items with custom layouts:

```python
item = stackit.StackMenuItem(title="My Item")

# Create layout
layout = item.hstack(spacing=8)
layout.append(stackit.label("Status:"))
layout.append(stackit.spacer())
layout.append(stackit.label("Online", color="green"))

# Apply layout
item.set_root_stack(layout)
```

### 3. Layouts - hstack & vstack

Arrange UI elements horizontally or vertically (like SwiftUI):

```python
# Horizontal layout
hstack = item.hstack(spacing=8)
hstack.append(label1)
hstack.append(button1)
hstack.append(spacer)

# Vertical layout
vstack = item.vstack(spacing=4)
vstack.append(title_label)
vstack.append(subtitle_label)
vstack.append(progress_bar)

# Nested layouts
main = item.vstack()
header = item.hstack()
header.extend([icon, title, spacer, close_button])
main.append(header)
main.append(content_vstack)
```

### 4. Controls - Rich UI Components

StackIt provides a comprehensive set of controls:

#### Text Controls
```python
stackit.label("Hello", font_size=14, bold=True, color="blue")
stackit.link("Visit Site", url="https://example.com")
```

#### Input Controls
```python
stackit.text_field(width=200, placeholder="Enter text")
stackit.secure_text_input(width=200, placeholder="Password")
stackit.search_field(width=200, placeholder="Search...")
```

#### Buttons & Selection
```python
stackit.button("Click Me", target=self, action="clicked:")
stackit.checkbox("Enable feature", state=True)
stackit.radio_button("Option 1", state=False)
stackit.combobox(items=["Option 1", "Option 2"], width=200)
```

#### Progress Indicators
```python
stackit.progress_bar(width=200, value=0.5)
stackit.circular_progress(size=32, indeterminate=True)
stackit.slider(width=150, min_value=0, max_value=100, value=50)
```

#### Date & Time
```python
stackit.date_picker(date=datetime.now(), date_only=True)
stackit.time_picker(time=datetime.now())
```

#### Layout Helpers
```python
stackit.spacer()  # Flexible spacer
stackit.separator(width=200)  # Visual separator
```

#### Images & Icons
```python
# From file
stackit.image("/path/to/image.png", width=24, height=24)

# From SF Symbol
icon = stackit.SFSymbol.create("star.fill", size=16, color="yellow")
stackit.image(icon, width=16, height=16)

# From URL
stackit.image("https://example.com/logo.png", width=32, height=32)
```

### 5. SF Symbols - Apple's Icon System

Full support for SF Symbols with extensive customization:

```python
# Basic symbol
icon = stackit.SFSymbol.create("star.fill")

# With size and weight
icon = stackit.SFSymbol.create("gear", size=20, weight="bold")

# With color
icon = stackit.SFSymbol.create("heart.fill", size=16, color="red")

# Advanced rendering modes
icon = stackit.SFSymbol.create(
    "gauge.badge.plus",
    size=24,
    weight="semibold",
    rendering_mode="hierarchical"
)

# Multicolor symbols
icon = stackit.SFSymbol.create(
    "brain.head.profile",
    size=32,
    rendering_mode="multicolor"
)

# Palette mode with multiple colors
icon = stackit.SFSymbol.create(
    "circle.hexagongrid.circle",
    size=24,
    rendering_mode="palette",
    color="blue",
    secondary_color="red",
    tertiary_color="yellow"
)
```

**Weight options:** ultraLight, thin, light, regular, medium, semibold, bold, heavy, black
**Rendering modes:** automatic, monochrome, hierarchical, palette, multicolor
**Scale options:** small, medium, large

Browse symbols at: https://developer.apple.com/sf-symbols/

### 6. Utilities - Helper Functions

```python
# Alerts
result = stackit.alert("Title", "Message", ok="Yes", cancel="No")

# Notifications
stackit.notification("Title", "Subtitle", "Message body")

# Timers
timer = stackit.every(5.0, callback_function)  # Repeating
timer = stackit.after(2.0, callback_function)  # One-shot

# File selection
path = stackit.choose_directory(title="Select Folder")

# Preferences
stackit.save_preferences("MyApp", {"key": "value"})
prefs = stackit.load_preferences("MyApp", defaults={"key": "default"})

# Application control
stackit.quit_application()
```

---

## 🎯 Real-World Examples

### System Monitor

```python
import stackit
import psutil

class SystemMonitor:
    def __init__(self):
        self.app = stackit.StackApp("💻 System")
        self.setup_ui()
        self.timer = stackit.every(3.0, self.update)

    def setup_ui(self):
        self.item = stackit.StackMenuItem("Stats")
        self.app.add_item("stats", self.item)

    def update(self, timer):
        cpu = psutil.cpu_percent() / 100.0
        mem = psutil.virtual_memory().percent / 100.0

        layout = self.item.vstack(spacing=6)

        # CPU
        layout.append(stackit.label("CPU", font_size=11, bold=True))
        layout.append(stackit.progress_bar(width=180, value=cpu))

        # Memory
        layout.append(stackit.label("Memory", font_size=11, bold=True))
        layout.append(stackit.progress_bar(width=180, value=mem))

        self.item.set_root_stack(layout)

    def run(self):
        self.update(None)
        self.app.run()

if __name__ == "__main__":
    SystemMonitor().run()
```

### Network Status Indicator

```python
import stackit
import subprocess

class NetworkMonitor:
    def __init__(self):
        self.app = stackit.StackApp("Net")
        self.connected = True
        self.setup_ui()
        stackit.every(30.0, self.check_network)
        self.check_network(None)

    def setup_ui(self):
        self.item = stackit.StackMenuItem("Status")
        self.app.add_item("status", self.item)

    def check_network(self, timer):
        try:
            subprocess.check_call(
                ["ping", "-c", "1", "8.8.8.8"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )
            self.connected = True
        except:
            self.connected = False

        # Update UI
        layout = self.item.hstack(spacing=8)

        icon_name = "wifi" if self.connected else "wifi.slash"
        color = "green" if self.connected else "red"

        icon = stackit.image(
            stackit.SFSymbol.create(icon_name, size=16, color=color),
            width=16, height=16
        )
        layout.append(icon)
        layout.append(stackit.label(
            "Connected" if self.connected else "Disconnected",
            color=color
        ))

        self.item.set_root_stack(layout)

        # Update app icon
        self.app.set_icon(stackit.SFSymbol.create(icon_name, size=16))

    def run(self):
        self.app.run()

if __name__ == "__main__":
    NetworkMonitor().run()
```

### Timer App

```python
import stackit
import time

class TimerApp:
    def __init__(self):
        self.app = stackit.StackApp("Timer", "⏱")
        self.start_time = time.time()
        self.setup_ui()
        stackit.every(1.0, self.update)

    def setup_ui(self):
        self.item = stackit.StackMenuItem("Time")
        self.app.add_item("time", self.item)

        # Reset button
        reset = stackit.StackMenuItem("Reset")
        layout = reset.hstack()
        layout.append(stackit.button("🔄 Reset", target=self, action="reset:"))
        reset.set_root_stack(layout)
        self.app.add_item("reset", reset)

    def update(self, timer):
        elapsed = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed, 60)

        layout = self.item.hstack(spacing=8)
        layout.append(stackit.label("Time:", bold=True))
        layout.append(stackit.spacer())
        layout.append(stackit.label(f"{minutes:02d}:{seconds:02d}", font_size=14))
        self.item.set_root_stack(layout)

    def reset_(self, sender):
        self.start_time = time.time()

    def run(self):
        self.update(None)
        self.app.run()

if __name__ == "__main__":
    TimerApp().run()
```

---

## 📖 Documentation

Full documentation is available in the `docs/` directory:

- **[Installation Guide](docs/installation.rst)** - Setup and requirements
- **[Quick Start](docs/quickstart.rst)** - Get started quickly
- **[API Reference](docs/api/index.rst)** - Complete API documentation
  - [Core](docs/api/core.rst) - StackApp, StackMenuItem, StackView
  - [Controls](docs/api/controls.rst) - All UI controls
  - [SF Symbols](docs/api/sfsymbol.rst) - SF Symbol support
  - [Utils](docs/api/utils.rst) - Utility functions
  - [Delegate](docs/api/delegate.rst) - Application lifecycle
- **[Examples](docs/examples.rst)** - Complete working examples

### Building Documentation

```bash
cd docs
pip install sphinx sphinx-rtd-theme
make html
open _build/html/index.html
```

---

## 🏗️ Project Structure

```
stackit/
├── __init__.py          # Main exports and API
├── core.py              # StackApp, StackMenuItem, StackView
├── controls.py          # UI control creation functions
├── sfsymbol.py          # SF Symbol support
├── utils.py             # Utility functions (alerts, timers, etc.)
├── delegate.py          # Application delegate (lifecycle)
├── docs/                # Sphinx documentation
│   ├── index.rst
│   ├── installation.rst
│   ├── quickstart.rst
│   ├── examples.rst
│   └── api/
│       ├── core.rst
│       ├── controls.rst
│       ├── sfsymbol.rst
│       ├── utils.rst
│       └── delegate.rst
├── examples/            # Example applications
└── README.md
```

---

## 🎨 Design Philosophy

1. **Native First** - Built directly on AppKit for true native macOS integration
2. **Modern API** - SwiftUI-inspired layouts (hstack/vstack) with Pythonic syntax
3. **Zero Bloat** - No unnecessary dependencies, minimal footprint
4. **Flexibility** - From simple status indicators to complex dashboards
5. **Developer Experience** - Intuitive, well-documented, easy to learn

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and create pull requests.

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🌟 Use Cases

StackIt is perfect for:

- **System Monitors** - CPU, memory, disk, network status
- **Development Tools** - Build status, test results, CI/CD indicators
- **Productivity Apps** - Timers, todo lists, quick notes
- **Media Controllers** - Music players, volume controls, podcast managers
- **Quick Actions** - Shortcuts, utilities, toggles, launchers
- **Status Indicators** - Service health, API status, background tasks
- **Information Dashboards** - Weather, stocks, crypto prices, news feeds

---

## 🔗 Comparison with rumps

**StackIt is NOT based on rumps.** It's a completely standalone framework with:

- ✅ No rumps dependency - built directly on PyObjC/AppKit
- ✅ Rich custom layouts - hstack/vstack for complex UIs
- ✅ More controls - extensive UI component library
- ✅ Better SF Symbols support - full customization
- ✅ Modern API design - declarative, composable layouts

If you're looking for a simple, rumps-like API, rumps is great. If you need rich, custom layouts with advanced UI controls, StackIt is for you.

---

## 💡 Tips & Tricks

### Dynamic Updates

Update menu items in real-time by recreating their layout:

```python
def update_status(self):
    item = self.app.get_item("status")
    new_layout = item.hstack()
    new_layout.append(stackit.label(f"Status: {self.current_status}"))
    item.set_root_stack(new_layout)
```

### Callback Actions

Use target/action pattern for button callbacks:

```python
# In your class
def button_clicked_(self, sender):
    print("Button clicked!")

# When creating button
btn = stackit.button("Click", target=self, action="button_clicked:")
```

Note: Action names must end with `:` and the method must end with `_`

### Spacers for Alignment

Use spacers to push elements to opposite ends:

```python
layout = item.hstack()
layout.append(stackit.label("Left"))
layout.append(stackit.spacer())  # Pushes everything after to the right
layout.append(stackit.label("Right"))
```

### Complex Nested Layouts

Build sophisticated UIs with nested stacks:

```python
main = item.vstack(spacing=8)

# Header row
header = item.hstack()
header.append(icon)
header.append(title)
header.append(stackit.spacer())
header.append(close_btn)
main.append(header)

# Content section
content = item.vstack(spacing=4)
content.append(subtitle)
content.append(progress)
content.append(status_text)
main.append(content)

# Footer with buttons
footer = item.hstack()
footer.append(stackit.spacer())
footer.append(cancel_btn)
footer.append(ok_btn)
main.append(footer)

item.set_root_stack(main)
```

---

**Built with ❤️ for the macOS developer community**

Give StackIt a ⭐ if you find it useful!
