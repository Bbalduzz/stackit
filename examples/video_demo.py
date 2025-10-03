#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Video Player Demo - Demonstrates the video() control using AVKit

This example shows how to embed a video player in a menu bar app.
You can use either local video files or remote URLs.
"""

import sys
import os

# Add parent directory to path for development
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import stackit

def main():
    # Create the app
    app = stackit.StackApp(
        title="Video Player",
        icon=stackit.SFSymbol("play.rectangle.fill", color="#FF6B6B")
    )

    # Example video URLs - replace with your own video file path or URL
    # For testing, you can use Apple's sample videos or any video URL
    sample_video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

    # Alternatively, use a local file:
    # local_video_path = "/path/to/your/video.mp4"
    # video_player = stackit.video(local_video_path, dimensions=(400, 300))

    # Create video player with controls
    video_with_controls = stackit.video(
        sample_video_url,
        dimensions=(400, 225),
        border_radius=12.0,
        show_controls=True,
        autoplay=False,
        loop=False
    )

    # Create menu item with video
    video_item = stackit.MenuItem(
        layout=stackit.vstack([
            stackit.label("Video Player Demo", bold=True, font_size=14),
            stackit.separator(),
            video_with_controls,
            stackit.separator(),
            stackit.label("Sample video from the internet", font_size=10, color="gray"),
        ], spacing=8)
    )

    app.add(video_item)

    # Add info item
    info_item = stackit.MenuItem(
        layout=stackit.vstack([
            stackit.label("Video Control Features:", bold=True),
            stackit.label("• Supports local and remote videos", font_size=11),
            stackit.label("• Built-in playback controls", font_size=11),
            stackit.label("• Autoplay and loop options", font_size=11),
            stackit.label("• Powered by AVKit", font_size=11),
        ], spacing=4)
    )

    app.add(info_item)

    # Run the app
    app.run()


if __name__ == '__main__':
    main()
