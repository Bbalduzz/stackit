# StackIt - Isolated StackMenuItem Framework

A completely isolated framework for creating macOS statusbar applications using only StackMenuItem for rich layouts. No dependencies on the main rumps library.

## 🎯 Overview

StackIt provides a minimal, focused API for building statusbar apps with rich, custom layouts using only the StackMenuItem concept. It's designed to be:

- **Isolated**: No dependencies on main rumps library
- **Focused**: Only StackMenuItem functionality
- **Rich**: Complex layouts with hstack/vstack
- **Simple**: Clean, intuitive API

## 📁 Structure

```
stackit/
├── __init__.py          # Main exports
├── core.py              # Core StackMenuItem and StackApp classes
├── utils.py             # Utility functions (alert, notification, etc.)
├── components.py        # Component factory functions
├── examples/
│   ├── basic_example.py    # Basic usage patterns
│   ├── factory_example.py  # Factory function demos
│   └── advanced_example.py # Advanced patterns with timers
└── README.md           # This file
```

## 🚀 Quick Start

### Basic Usage

```python
import stackit

# Create app
app = stackit.StackApp.stackAppWithTitle_icon_("My App", "📱")

# Create a stack menu item
item = stackit.StackMenuItem.stackMenuItemWithTitle_callback_("Hello", None)

# Build layout
main_stack = item.hstack()
main_stack.append(item.label("Hello, World!", bold=True))
main_stack.append(item.spacer())
main_stack.append(item.button("Click", target=app, action="clicked:"))

# Set layout and add to app
item.set_root_stack(main_stack)
app.add_item("hello", item)

# Run
app.run()
```

### Using Factory Functions

```python
import stackit
from stackit.components import create_list_tile, create_status_item

app = stackit.StackApp.stackAppWithTitle_icon_("Factory Demo", "🏭")

# Quick list tile
tile = create_list_tile(
    title_text="Download Progress",
    subtitle_text="75% complete",
    action_title="Pause",
    target=self,
    action="pause_download:"
)
app.add_item("download", tile)

# Status item
status = create_status_item(
    title="Server",
    status="Connected",
    action_title="Disconnect",
    target=self,
    action="disconnect:"
)
app.add_item("status", status)

app.run()
```

## 🏗️ Core Components

### StackApp

The main application class for managing statusbar apps.

```python
# Create app
app = stackit.StackApp.stackAppWithTitle_icon_("Title", "icon.png")

# Add items
app.add_item("key", stack_menu_item)
app.add_separator()

# Manage items
item = app.get_item("key")
app.remove_item("key")

# Set icon/title
app.set_title("New Title")
app.set_icon("new_icon.png")

# Run app
app.run()
```

### StackMenuItem

Rich menu items with custom layouts.

```python
# Create item
item = stackit.StackMenuItem.stackMenuItemWithTitle_callback_("Title", callback)

# Create layouts
h_stack = item.hstack(alignment=NSLayoutAttributeCenterY, spacing=8)
v_stack = item.vstack(alignment=NSLayoutAttributeLeading, spacing=4)

# Add UI elements
label = item.label("Text", font_size=13, bold=True, color="gray")
button = item.button("Click", target=self, action="action:")
image = item.image_view("icon.png", width=24, height=24)
spacer = item.spacer(priority=250)

# Build layout
h_stack.extend([image, label, spacer, button])

# Set root layout
item.set_root_stack(h_stack)
```

### StackView

Container for arranging UI elements.

```python
# Create stacks
hstack = stackit.hstack(spacing=8, views=[view1, view2])
vstack = stackit.vstack(spacing=4)

# Manipulate like a list
stack.append(view)
stack.extend([view1, view2, view3])
stack.insert(1, view)
stack.remove(view)
stack.clear()
```

## 🎨 UI Components

### Labels

```python
# Basic label
label = item.label("Hello World")

# Styled label
title = item.label("Title", font_size=16, bold=True)
subtitle = item.label("Subtitle", font_size=12, color="gray")
```

### Buttons

```python
# Basic button
btn = item.button("Click Me", target=self, action="clicked:")

# Buttons automatically get proper hugging priority
```

### Images

```python
# File-based image
icon = item.image_view("/path/to/icon.png", width=24, height=24)

# System image
sys_icon = item.image_view("NSActionTemplate", width=16, height=16)

# With scaling
image = item.image_view("image.png", scaling=NSImageScaleNone)
```

### Spacers

```python
# Flexible spacer (expands to fill space)
spacer = item.spacer()

# Custom priority spacer
spacer = item.spacer(priority=100)  # Higher priority = less expansion
```

## 🏭 Factory Functions

Pre-built patterns for common UI layouts.

### List Tiles

```python
from stackit.components import create_list_tile

tile = create_list_tile(
    title_text="Main Title",
    subtitle_text="Optional subtitle",
    icon_path="/path/to/icon.png",        # Optional
    action_title="Action",                # Optional
    target=self,                         # Optional
    action="action_method:"              # Optional
)
```

### Status Items

```python
from stackit.components import create_status_item

status = create_status_item(
    title="Connection",
    status="Connected",
    color="gray",                        # Optional
    action_title="Disconnect",           # Optional
    target=self,                        # Optional
    action="disconnect:"                 # Optional
)
```

### Info Cards

```python
from stackit.components import create_info_card

card = create_info_card(
    title="Card Title",
    subtitle="Card Subtitle",
    body="Detailed information about the card",
    action_title="Learn More",           # Optional
    target=self,                        # Optional
    action="learn_more:"                 # Optional
)
```

## 🛠️ Utilities

### Alerts

```python
# Basic alert
stackit.alert("Title", "Message")

# Alert with buttons
result = stackit.alert("Title", "Message", ok="Yes", cancel="No")
if result == 1:  # OK clicked
    print("User clicked Yes")
```

### Notifications

```python
# Basic notification
stackit.notification("Title", "Subtitle", "Message")

# Without sound
stackit.notification("Title", message="Silent message", sound=False)
```

### Other Utilities

```python
# Quit application
stackit.quit_application()

# Open URL
stackit.open_url("https://example.com")

# Run shell command
code, stdout, stderr = stackit.run_command(["ls", "-la"])

# Preferences
stackit.save_preferences("MyApp", {"key": "value"})
prefs = stackit.load_preferences("MyApp", defaults={"key": "default"})

# Timers
timer = stackit.create_timer(5.0, callback_function, repeats=True)
```

## 📱 Layout Patterns

### Horizontal Layouts

```python
# Icon + Text + Button
row = item.hstack()
row.append(item.image_view("icon.png", width=16, height=16))
row.append(item.label("Status: Connected"))
row.append(item.spacer())
row.append(item.button("Disconnect", target=self, action="disconnect:"))
```

### Vertical Layouts

```python
# Title + Subtitle + Actions
col = item.vstack(spacing=4)
col.append(item.label("Main Title", font_size=14, bold=True))
col.append(item.label("Subtitle text", font_size=11, color="gray"))

# Action buttons in horizontal row
actions = item.hstack()
actions.append(item.button("Cancel", target=self, action="cancel:"))
actions.append(item.spacer())
actions.append(item.button("OK", target=self, action="ok:"))
col.append(actions)
```

### Complex Layouts

```python
# Dashboard-style layout
main = item.vstack(spacing=8)

# Header with icon and title
header = item.hstack()
header.append(item.label("📊", font_size=16))
header.append(item.label("Dashboard", font_size=14, bold=True))
header.append(item.spacer())
header.append(item.button("↻", target=self, action="refresh:"))

# Metrics rows
cpu_row = item.hstack()
cpu_row.append(item.label("CPU:", font_size=11, bold=True))
cpu_row.append(item.spacer())
cpu_row.append(item.label("25%", font_size=11, color="gray"))

memory_row = item.hstack()
memory_row.append(item.label("Memory:", font_size=11, bold=True))
memory_row.append(item.spacer())
memory_row.append(item.label("8.2 GB", font_size=11, color="gray"))

main.extend([header, cpu_row, memory_row])
item.set_root_stack(main)
```

## 🔄 Dynamic Updates

StackIt supports dynamic updates to menu items:

```python
def update_status(self):
    """Update an existing menu item's layout."""
    item = self.app.get_item("status")

    # Create new layout
    new_stack = item.hstack()
    new_stack.append(item.label("Updated Status", bold=True))

    # Replace existing layout
    item.set_root_stack(new_stack)

def timer_callback(self, timer):
    """Called by timer to update UI."""
    self.counter += 1
    self.update_counter_display()

# Set up timer
self.timer = stackit.create_timer(1.0, self.timer_callback, repeats=True)
```

## 📋 Examples

See the `examples/` directory for complete working examples:

- **`basic_example.py`** - Basic usage patterns and simple layouts
- **`factory_example.py`** - Using factory functions for common UI patterns
- **`advanced_example.py`** - Advanced patterns with timers and dynamic updates

Run examples:

```bash
cd stackit/examples
python3 basic_example.py
python3 factory_example.py
python3 advanced_example.py
```

## 🎯 Use Cases

StackIt is perfect for:

- **System monitors** - CPU, memory, network status
- **Development tools** - Build status, test results
- **Productivity apps** - Todo lists, timers, notifications
- **Media controllers** - Music players, volume controls
- **Quick actions** - Shortcuts, utilities, toggles

## 🔧 Integration

StackIt is completely isolated and can be used alongside other frameworks or as a standalone solution. It requires only:

- macOS 10.14+
- Python 3.7+
- PyObjC (usually comes with macOS Python)

## 🎉 Benefits

- **Rich layouts** without complex UI frameworks
- **Native performance** using AppKit directly
- **Small footprint** - isolated, minimal dependencies
- **Familiar patterns** - hstack/vstack like SwiftUI
- **Flexible** - from simple to complex layouts
- **Maintainable** - clean separation of concerns

StackIt gives you the power of StackMenuItem in a focused, easy-to-use package! 🚀