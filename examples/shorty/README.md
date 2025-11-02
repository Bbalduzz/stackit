# Shorty - Minimal Global Shortcuts Manager

A StackIt-based macOS menu bar app for user-defined global shortcuts with minimal UI.

## Features

- **Global Hotkeys**: System-wide keyboard shortcuts that work from any application (via pynput)
- **Minimal UI**: Clean menu bar interface showing shortcuts with key_equivalent display
- **Built-in Actions**: Common actions like opening Terminal, iTerm2, or creating text files
- **Custom Commands**: Execute any shell command via shortcut
- **Config Storage**: Shortcuts saved to `~/.config/shorty/shortcuts.json`
- **Simple Design**: No complex UI - just MenuItem entries with keyboard shortcuts displayed

## Installation

1. Install the required dependency:
```bash
pip install pynput
```

2. Run the application:
```bash
python3 shorty.py
```

## Default Shortcuts

The app comes with these pre-configured shortcuts (Cmd+key):

- **Cmd+Enter**: Open new Terminal window
- **Cmd+T**: Create new text file in TextEdit
- **Cmd+I**: Open new iTerm2 window

## Usage

### Running the App
```bash
cd examples/shorty
python3 shorty_setup.py
```

The app will appear in your menu bar with a command symbol (⚡).

### Managing Shortcuts

1. **View Status**: Click the menu bar icon to see all configured shortcuts
2. **Toggle Shortcuts**: Click "Toggle" next to any shortcut to enable/disable it
3. **Remove Shortcuts**: Click "Remove" to delete a shortcut
4. **Add Shortcuts**: Click "Add Shortcut" (currently adds a demo shortcut)
5. **Reload**: Click "Reload" to restart the hotkey listener

### Custom Actions

You can edit the shortcuts file directly:
```bash
open ~/.shorty_shortcuts.json
```

#### Action Types

1. **Built-in Actions**:
   - `"terminal"`: Opens new Terminal window
   - `"iterm"`: Opens new iTerm2 window
   - `"text_file"`: Creates new TextEdit document

2. **Custom Commands**:
   - `"command:your-shell-command"`: Execute any shell command
   - Example: `"command:open -a 'Visual Studio Code'"`

#### Shortcut Format

Shortcuts use pynput format:
- `<cmd>`: Command key
- `<alt>`: Option key
- `<shift>`: Shift key
- `<ctrl>`: Control key
- Letter keys: `a`, `b`, `c`, etc.
- Special keys: `<enter>`, `<space>`, `<tab>`, etc.

Example configuration:
```json
{
  "<cmd>+<shift>+v": {
    "name": "Open VS Code",
    "action": "command:open -a 'Visual Studio Code'",
    "description": "Launch Visual Studio Code",
    "enabled": true
  }
}
```

## Permissions

macOS may require you to grant accessibility permissions for global hotkeys:

1. Go to **System Preferences** > **Security & Privacy** > **Privacy**
2. Select **Accessibility** from the left panel
3. Add Terminal (or your Python executable) to the allowed applications
4. Restart the app

## Troubleshooting

### Hotkeys Not Working
- Check that accessibility permissions are granted
- Verify the shortcut format in the JSON file
- Restart the app after making changes

### App Won't Start
- Make sure pynput is installed: `pip install pynput`
- Check for Python version compatibility (Python 3.7+)

### Conflicting Shortcuts
- Some shortcuts may conflict with system shortcuts
- Try different key combinations if a shortcut doesn't work

## File Structure

```
shorty/
├── shorty_setup.py    # Main application file
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Configuration File

The app stores shortcuts in `~/.shorty_shortcuts.json`. You can edit this file directly or use the menu bar interface.

Example configuration structure:
```json
{
  "<cmd>+<enter>": {
    "name": "New Terminal",
    "action": "terminal",
    "description": "Open new Terminal window",
    "enabled": true
  }
}
```

## Development

To extend Shorty with new actions:

1. Add action handling in `execute_action()` method
2. Update the default shortcuts if needed
3. Consider adding UI for custom action creation

## License

This example is part of the StackIt framework examples.