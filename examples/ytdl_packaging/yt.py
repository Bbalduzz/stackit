import sys
import os
import threading
import logging
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import stackit
from pytubefix import YouTube
from AppKit import NSPasteboard, NSImage, NSBezierPath, NSColor, NSGraphicsContext
from Foundation import NSMakeRect, NSMakeSize
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)

class YTDLPApp(stackit.StackApp):
    def __init__(self):
        # Use objc.super for Objective-C inheritance
        super(YTDLPApp, self).__init__(icon=stackit.SFSymbol("arrow.down.circle.fill", rendering="hierarchical"))

        self.video_info = None
        self.menu_item = None
        self.search_field = None
        self.combobox = None
        self.progress_bar = None
        self.download_button = None
        self.last_processed_url = None
        self.yt = None
        self.is_downloading = False
        self._current_progress = 0.0

        # Load preferences
        prefs = stackit.load_preferences("ytdlp", defaults={"download_directory": os.path.expanduser("~/Downloads")})
        self.download_directory = prefs.get("download_directory", os.path.expanduser("~/Downloads"))
        logging.info(f"📁 Download directory: {self.download_directory}")

    def setup_menu(self):
        self.menu_item = stackit.MenuItem()

        # Title section
        self.settings_button = stackit.button(
            image=stackit.SFSymbol("gear"),
            image_position="only",
            target=self,
            action="openSettings:"
        )

        self.title_stack = stackit.hstack([
            stackit.image(stackit.SFSymbol("arrow.down.circle.dotted")),
            stackit.label("Youtube downloader", font_size=13),
            stackit.spacer(),
            self.settings_button
        ])

        # Search field
        self.search_field = stackit.search_field(
            placeholder="Paste YouTube URL here",
            target=self,
            action="processURL:",
            size=(300, 30)
        )

        # Preview section - starts with placeholder label
        self.preview_container = stackit.vstack([
            stackit.label("Enter a YouTube URL to preview", font_size=10, width=200, color="gray")
        ], spacing=5)

        # Status section - for progress bar or completion messages
        self.status_container = stackit.vstack([], spacing=30)

        # Options and download controls
        self.combobox = stackit.combobox(
            items=["Best Quality", "Only Audio (mp3)", "Dump JSON Info"],
            selected_index=0,
            width=120,
        )

        self.download_button = stackit.button(
            title="Download",
            target=self,
            action="downloadMedia:"
        )
        self.download_button.setEnabled_(False)

        self.options_stack = stackit.hstack([
            stackit.spacer(),
            self.combobox,
            self.download_button
        ])

        # Main container - this stays constant
        self.main_stack = stackit.vstack([
            self.title_stack,
            self.search_field,
            stackit.block(self.preview_container),
            self.options_stack,
            self.status_container
        ], spacing=10)

        self.menu_item.set_layout(self.main_stack)
        self.add(self.menu_item)

        # Check pasteboard on startup
        self.check_pasteboard()

    def check_pasteboard(self):
        """Check pasteboard for YouTube URL and auto-process if found"""
        pasteboard = NSPasteboard.generalPasteboard()
        url = pasteboard.stringForType_("public.utf8-plain-text")

        if url and self.is_youtube_url(url):
            if url != self.last_processed_url:
                logging.info(f"📋 New YouTube URL detected: {url[:50]}...")
                self.last_processed_url = url
                self.search_field.setStringValue_(url)
                self.process_url(url)

    def is_youtube_url(self, url):
        """Check if URL is a valid YouTube URL"""
        return 'youtube.com' in url or 'youtu.be' in url

    def create_progress_ring_image(self, progress):
        """Create a circular progress ring image for the status bar"""
        size = 20.0  # Status bar icon size
        image = NSImage.alloc().initWithSize_(NSMakeSize(size, size))

        image.lockFocus()

        # Calculate the rect for the ring
        rect = NSMakeRect(2, 2, size - 4, size - 4)
        center_x = size / 2
        center_y = size / 2
        radius = (size - 4) / 2

        # Background circle (light gray)
        NSColor.colorWithWhite_alpha_(0.3, 0.3).set()
        bg_path = NSBezierPath.alloc().init()
        bg_path.appendBezierPathWithOvalInRect_(rect)
        bg_path.setLineWidth_(2.5)
        bg_path.stroke()

        # Progress arc (blue/accent color)
        if progress > 0:
            NSColor.colorWithRed_green_blue_alpha_(0.31, 0.80, 0.77, 1.0).set()  # #4ECDC4
            progress_path = NSBezierPath.alloc().init()

            # Start from top (270 degrees in AppKit coordinate system)
            start_angle = 90
            end_angle = 90 - (progress * 360)

            progress_path.appendBezierPathWithArcWithCenter_radius_startAngle_endAngle_clockwise_(
                (center_x, center_y),
                radius,
                start_angle,
                end_angle,
                True  # clockwise
            )
            progress_path.setLineWidth_(2.5)
            progress_path.setLineCapStyle_(1)  # Round cap
            progress_path.stroke()

        # Download arrow in center
        arrow_color = NSColor.colorWithWhite_alpha_(0.9, 1.0) if progress < 1.0 else NSColor.colorWithRed_green_blue_alpha_(0.31, 0.80, 0.77, 1.0)
        arrow_color.set()
        arrow_path = NSBezierPath.alloc().init()

        # Draw simple down arrow
        arrow_size = 6
        arrow_path.moveToPoint_((center_x, center_y + arrow_size/2))
        arrow_path.lineToPoint_((center_x, center_y - arrow_size/2))
        arrow_path.moveToPoint_((center_x - arrow_size/3, center_y - arrow_size/4))
        arrow_path.lineToPoint_((center_x, center_y - arrow_size/2))
        arrow_path.lineToPoint_((center_x + arrow_size/3, center_y - arrow_size/4))
        arrow_path.setLineWidth_(1.8)
        arrow_path.setLineCapStyle_(1)
        arrow_path.stroke()

        image.unlockFocus()

        # Set template to use system accent color
        image.setTemplate_(False)

        return image

    def openSettings_(self, sender):
        """Open settings dialog to choose download directory"""
        logging.info("⚙️  Opening settings...")

        selected_dir = stackit.choose_directory(
            title="Choose Download Directory",
            default_directory=self.download_directory
        )

        if selected_dir:
            self.download_directory = selected_dir
            logging.info(f"📁 Download directory updated: {self.download_directory}")

            # Save preference
            stackit.save_preferences("ytdlp", {"download_directory": self.download_directory})
            logging.info("💾 Preferences saved")

    def processURL_(self, sender):
        """Called when user enters URL in search field"""
        url = sender.stringValue()
        if not url:
            logging.warning("⚠️  Empty URL provided")
            return

        logging.info(f"⌨️  Manual URL entered: {url}")
        self.process_url(url)

    def process_url(self, url):
        """Process a YouTube URL"""
        logging.info(f"🔄 Processing URL: {url}")

        # Update preview to show loading
        self.preview_container.clear()
        loading_label = stackit.label("Loading video info...", font_size=10, color="gray")
        self.preview_container.append(loading_label)

        # Fetch video info in background
        def fetch_info():
            try:
                logging.info("🌐 Fetching video info from YouTube...")

                # Create YouTube object with progress callback
                self.yt = YouTube(
                    url,
                    on_progress_callback=self.on_progress,
                    on_complete_callback=self.on_complete
                )

                # Store video info
                self.video_info = {
                    'title': self.yt.title,
                    'uploader': self.yt.author,
                    'duration': self.yt.length,
                    'thumbnail': self.yt.thumbnail_url,
                    'webpage_url': url,
                    'views': self.yt.views,
                    'description': self.yt.description
                }

                logging.info(f"✅ Video info fetched: {self.yt.title}")

                # Update UI on main thread
                self.performSelectorOnMainThread_withObject_waitUntilDone_(
                    "updatePreview:",
                    None,
                    False
                )

            except Exception as e:
                logging.error(f"❌ Error fetching video info: {e}")
                # Update UI with error
                self.performSelectorOnMainThread_withObject_waitUntilDone_(
                    "showError:",
                    None,
                    False
                )

        thread = threading.Thread(target=fetch_info, daemon=True)
        thread.start()

    def updatePreview_(self, timer=None):
        """Update preview with video info (runs on main thread)"""
        if not self.video_info:
            logging.warning("⚠️  No video info available")
            return

        # Get video details
        title = self.video_info.get('title', 'Unknown Title')
        channel = self.video_info.get('uploader', 'Unknown Channel')
        duration = self.video_info.get('duration', 0)

        logging.info(f"🎬 Updating preview - Title: {title}")
        logging.info(f"👤 Channel: {channel}")
        logging.info(f"⏱️  Duration: {duration}s")
        thumbnail_url = self.video_info.get('thumbnail', '')

        # Format duration
        minutes = duration // 60
        seconds = duration % 60
        duration_str = f"{minutes}:{seconds:02d}"

        # Create preview content
        self.video_preview = stackit.hstack([
            stackit.image(thumbnail_url, width=100, border_radius=8) if thumbnail_url else stackit.spacer(),
            stackit.vstack([
                stackit.label(title, font_size=11, width=180, bold=True, wraps=True),
                stackit.hstack([
                    stackit.label(channel, font_size=9, color="gray"),
                    stackit.label("-", font_size=9),
                    stackit.label(duration_str, font_size=9, color="gray")
                ])
            ])
        ])

        # Clear preview container and add video preview
        self.preview_container.clear()
        self.preview_container.append(self.video_preview)

        # Force layout update
        self.preview_container.setNeedsLayout_(True)
        self.main_stack.setNeedsLayout_(True)

        # Enable download button
        self.download_button.setEnabled_(True)
        logging.info("✅ Preview updated, download button enabled")

    def showError_(self, timer):
        """Show error message (runs on main thread)"""
        logging.error("❌ Showing error message in UI")

        # Clear preview and show error message
        self.preview_container.clear()
        error_label = stackit.label("Error loading video. Check URL and try again.",
                                    font_size=10, color="gray")
        self.preview_container.append(error_label)


    def downloadMedia_(self, sender):
        """Called when download button is clicked"""
        if not self.video_info or not hasattr(self, 'yt'):
            logging.warning("⚠️  No video info available")
            return

        print("downloading media")

        selected_index = self.combobox.indexOfSelectedItem()
        options = ["Best Quality", "Only Audio (mp3)", "Dump JSON Info"]

        logging.info(f" Download started - Option: {options[selected_index]}")

        # Set downloading flag and reset progress
        self.is_downloading = True
        self._current_progress = 0.0

        # Disable download button during download
        self.download_button.setEnabled_(False)

        # Add progress bar to status container
        self.progress_bar = stackit.progress_bar(value=0.0, dimensions=(300, 20), show_text=False)
        self.status_container.clear()
        self.status_container.append(stackit.label("Downloading in progress:", color="gray", font_size=9))
        self.status_container.append(self.progress_bar)

        def download():
            try:
                if selected_index == 0:  # Best Quality
                    logging.info("Starting Best Quality download...")
                    self.download_best_quality()
                elif selected_index == 1:  # Only Audio (mp3)
                    logging.info("Starting Audio download...")
                    self.download_audio()
                elif selected_index == 2:  # Dump JSON Info
                    logging.info("Dumping JSON info...")
                    self.dump_json()
            except Exception as e:
                logging.error(f"❌ Download error: {e}")
            finally:
                # Re-enable button on main thread
                self.performSelectorOnMainThread_withObject_waitUntilDone_(
                    "downloadComplete:",
                    None,
                    False
                )

        thread = threading.Thread(target=download, daemon=True)
        thread.start()

    def on_progress(self, stream, chunk, bytes_remaining):
        """Progress callback for pytubefix"""
        try:
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percent = bytes_downloaded / total_size

            # Log progress every 10%
            if int(percent * 100) % 10 == 0:
                logging.info(f"📥 Progress: {int(percent * 100)}%")

            # Update progress bar on main thread
            self._current_progress = percent
            self.performSelectorOnMainThread_withObject_waitUntilDone_(
                "updateProgressBar:",
                None,
                False
            )
        except Exception as e:
            logging.debug(f"Progress update error: {e}")

    def on_complete(self, stream, file_path):
        """Complete callback for pytubefix"""
        logging.info(f"✅ Download finished: {file_path}")

    def updateProgressBar_(self, _):
        """Update progress bar UI (called on main thread)"""
        if hasattr(self, '_current_progress') and self.progress_bar:
            # Update progress bar
            for subview in self.progress_bar.subviews():
                if hasattr(subview, 'setDoubleValue_'):
                    subview.setDoubleValue_(self._current_progress)
                    break

            # Update status bar icon with dynamic progress ring
            if self.is_downloading:
                progress_ring = self.create_progress_ring_image(self._current_progress)
                self.set_icon(progress_ring)

    def download_best_quality(self):
        """Download video in best quality"""
        logging.info("🎥 Downloading video in best quality...")
        stream = self.yt.streams.get_highest_resolution()
        self.download_path = stream.download(output_path=self.download_directory)
        logging.info(f"✅ Best quality download complete: {self.download_path}")

    def download_audio(self):
        """Download audio only"""
        logging.info("🎵 Downloading audio only...")
        stream = self.yt.streams.get_audio_only()
        self.download_path = stream.download(output_path=self.download_directory)
        logging.info(f"✅ Audio download complete: {self.download_path}")

    def dump_json(self):
        """Dump video info to JSON file"""
        if self.video_info:
            filename = f"{self.video_info.get('title', 'video')}.json"
            filepath = os.path.join(self.download_directory, filename)
            logging.info(f"📄 Saving video info to: {filepath}")
            with open(filepath, 'w') as f:
                json.dump(self.video_info, f, indent=2)
            self.download_path = filepath
            logging.info(f"✅ Video info saved successfully: {self.download_path}")


    def downloadComplete_(self, timer):
        """Called when download is complete (runs on main thread)"""
        logging.info("✅ Download complete, updating UI")
        self.download_button.setEnabled_(True)

        # Reset downloading flag
        self.is_downloading = False

        # Reset status bar icon to default
        self.set_icon(stackit.SFSymbol("arrow.down.circle.fill", rendering="hierarchical"))

        # Clear progress bar
        self.status_container.clear()

        # Force layout update
        self.status_container.setNeedsLayout_(True)
        self.main_stack.setNeedsLayout_(True)

        # Send notification with file path
        file_path = getattr(self, 'download_path', 'Unknown location')
        stackit.notification(
            title="Download completed",
            message=file_path
        )

if __name__ == "__main__":
    app = YTDLPApp()
    app.setup_menu()

    # Check pasteboard every 2 seconds for new YouTube URLs
    stackit.every(2.0, lambda timer: app.check_pasteboard())

    app.run()