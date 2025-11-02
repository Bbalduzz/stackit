#!/usr/bin/env python3
"""
File Holder Demo - StacKit Example

A menu bar app that acts as a temporary file holder. You can:
1. Drop files into the menu bar area
2. View held files in the menu
3. Drag files out to other applications
4. Clear the file holder when done

This demonstrates drag and drop functionality with StacKit.
"""

import os, sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
import stackit
from pathlib import Path
from Foundation import NSPasteboard, NSFilenamesPboardType, NSURL
from AppKit import (
    NSDragOperationCopy, NSDragOperationNone, NSView, NSImage,
    NSImageView, NSTextField, NSColor, NSFont, NSBezierPath,
    NSCompositingOperationSourceOver
)
import objc


class FileDropView(NSView):
    """Custom view that accepts file drops"""

    def initWithCallback_(self, callback):
        self = objc.super(FileDropView, self).init()
        if self is None:
            return None

        self.callback = callback
        self.setWantsLayer_(True)
        self.layer().setCornerRadius_(8.0)
        self.layer().setBorderWidth_(2.0)
        self.layer().setBorderColor_(NSColor.tertiaryLabelColor().CGColor())
        self.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())

        # Register for drag types
        self.registerForDraggedTypes_([NSFilenamesPboardType])
        return self

    def draggingEntered_(self, sender):
        """Called when drag enters the view"""
        pboard = sender.draggingPasteboard()
        if pboard.availableTypeFromArray_([NSFilenamesPboardType]):
            self.layer().setBorderColor_(NSColor.systemBlueColor().CGColor())
            self.layer().setBackgroundColor_(NSColor.selectedContentBackgroundColor().CGColor())
            return NSDragOperationCopy
        return NSDragOperationNone

    def draggingExited_(self, sender):
        """Called when drag exits the view"""
        self.layer().setBorderColor_(NSColor.tertiaryLabelColor().CGColor())
        self.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())

    def performDragOperation_(self, sender):
        """Called when files are dropped"""
        pboard = sender.draggingPasteboard()
        files = pboard.propertyListForType_(NSFilenamesPboardType)

        if files and self.callback:
            self.callback(files)

        # Reset visual state
        self.draggingExited_(sender)
        return True


class DraggableFileView(NSView):
    """View that displays a file and allows dragging it out"""

    def initWithFilePath_(self, file_path):
        self = objc.super(DraggableFileView, self).init()
        if self is None:
            return None

        self.file_path = file_path
        self.setWantsLayer_(True)
        self.layer().setCornerRadius_(6.0)
        self.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())

        return self

    def mouseDown_(self, event):
        """Handle mouse down for drag initiation"""
        # Store the initial click point
        self.initial_location = event.locationInWindow()

    def mouseDragged_(self, event):
        """Handle mouse drag to initiate file drag"""
        current_location = event.locationInWindow()

        # Check if we've moved enough to start a drag
        dx = current_location.x - self.initial_location.x
        dy = current_location.y - self.initial_location.y
        distance = (dx * dx + dy * dy) ** 0.5

        if distance > 5.0:  # 5 pixel threshold
            self.startDragOperation_(event)

    def startDragOperation_(self, event):
        """Start dragging the file"""
        # Create pasteboard and add file
        pboard = NSPasteboard.pasteboardWithName_("NSDragPboard")
        pboard.declareTypes_owner_([NSFilenamesPboardType], None)
        pboard.setPropertyList_forType_([self.file_path], NSFilenamesPboardType)

        # Create drag image (file icon)
        image = NSImage.alloc().initWithSize_((32, 32))
        image.lockFocus()

        # Draw a simple file icon
        path = NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(
            ((2, 2), (28, 28)), 4.0, 4.0
        )
        NSColor.systemBlueColor().setFill()
        path.fill()

        image.unlockFocus()

        # Start the drag
        self.dragImage_at_offset_event_pasteboard_source_slideBack_(
            image,
            self.initial_location,
            (0, 0),
            event,
            pboard,
            self,
            True
        )


class FileHolder:
    """Main file holder application"""

    def __init__(self):
        self.held_files = []
        self.app = stackit.StackApp(
            title="File Holder",
            icon=stackit.SFSymbol("folder.badge.plus", color="#007AFF")
        )

        self.setup_ui()

    def setup_ui(self):
        """Set up the initial UI"""
        self.update_menu()

    def update_menu(self):
        """Update the menu with current files"""
        # Clear existing items
        self.app.menu.removeAllItems()

        if not self.held_files:
            # Show drop zone when no files
            drop_zone = self.create_drop_zone()
            empty_item = stackit.MenuItem(layout=stackit.vstack([
                stackit.label("📁 File Holder", bold=True, font_size=14),
                stackit.separator(),
                drop_zone,
                stackit.label("Drop files here to hold them temporarily",
                             color="gray", font_size=11)
            ], spacing=8))
            self.app.add(empty_item)
        else:
            # Show header
            header_item = stackit.MenuItem(layout=stackit.hstack([
                stackit.label("📁 File Holder", bold=True),
                stackit.spacer(),
                stackit.button("Clear All", callback=self.clear_all_files)
            ]))
            self.app.add(header_item)

            self.app.add(stackit.MenuItem.separator())

            # Show each file
            for i, file_path in enumerate(self.held_files):
                file_item = self.create_file_item(file_path, i)
                self.app.add(file_item)

            self.app.add(stackit.MenuItem.separator())

            # Add drop zone for more files
            drop_zone = self.create_drop_zone()
            drop_item = stackit.MenuItem(layout=stackit.vstack([
                drop_zone,
                stackit.label("Drop more files here", color="gray", font_size=10)
            ], spacing=4))
            self.app.add(drop_item)

        # Add default quit item
        self.app.add(stackit.MenuItem.separator())
        self.app.add(stackit.MenuItem(title="Quit", callback=self.quit_app, key_equivalent="q"))

        # Force menu update
        self.app.update()

    def create_drop_zone(self):
        """Create a file drop zone"""
        # Create the drop view
        drop_view = FileDropView.alloc().initWithCallback_(self.files_dropped)
        drop_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
        drop_view.widthAnchor().constraintEqualToConstant_(250).setActive_(True)
        drop_view.heightAnchor().constraintEqualToConstant_(60).setActive_(True)

        # Add label to the drop view
        label = NSTextField.labelWithString_("Drop files here")
        label.setTextColor_(NSColor.secondaryLabelColor())
        label.setFont_(NSFont.systemFontOfSize_(12))
        label.setAlignment_(1)  # Center alignment
        label.setTranslatesAutoresizingMaskIntoConstraints_(False)

        drop_view.addSubview_(label)

        # Center the label in the drop view
        label.centerXAnchor().constraintEqualToAnchor_(drop_view.centerXAnchor()).setActive_(True)
        label.centerYAnchor().constraintEqualToAnchor_(drop_view.centerYAnchor()).setActive_(True)

        return drop_view

    def create_file_item(self, file_path, index):
        """Create a menu item for a held file"""
        file_name = os.path.basename(file_path)
        file_size = self.get_file_size(file_path)

        # Create draggable file view
        drag_view = DraggableFileView.alloc().initWithFilePath_(file_path)
        drag_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
        drag_view.widthAnchor().constraintEqualToConstant_(20).setActive_(True)
        drag_view.heightAnchor().constraintEqualToConstant_(20).setActive_(True)

        layout = stackit.hstack([
            drag_view,
            stackit.vstack([
                stackit.label(file_name, bold=True),
                stackit.label(file_size, color="gray", font_size=10)
            ], spacing=2),
            stackit.spacer(),
            stackit.button("×", callback=lambda s: self.remove_file(index), width=20)
        ], spacing=8)

        return stackit.MenuItem(layout=layout)

    def get_file_size(self, file_path):
        """Get human-readable file size"""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        except:
            return "Unknown size"

    def files_dropped(self, file_paths):
        """Handle files being dropped"""
        for file_path in file_paths:
            if file_path not in self.held_files:
                self.held_files.append(file_path)

        self.update_menu()

        # Update status bar to show file count
        count = len(self.held_files)
        if count == 1:
            self.app.set_title("1 file")
        else:
            self.app.set_title(f"{count} files")

    def remove_file(self, index):
        """Remove a file from the holder"""
        if 0 <= index < len(self.held_files):
            self.held_files.pop(index)

            # Update status bar
            count = len(self.held_files)
            if count == 0:
                self.app.set_title("File Holder")
            elif count == 1:
                self.app.set_title("1 file")
            else:
                self.app.set_title(f"{count} files")

            self.update_menu()

    def clear_all_files(self, sender):
        """Clear all held files"""
        self.held_files.clear()
        self.app.set_title("File Holder")
        self.update_menu()

    def quit_app(self, sender):
        """Quit the application"""
        stackit.quit()

    def run(self):
        """Start the application"""
        self.app.run()


if __name__ == "__main__":
    app = FileHolder()
    app.run()