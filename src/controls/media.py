#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Media Controls - Video, Maps, and Web Views.

This module provides media control factory functions for creating rich media
experiences in StackIt applications including:
- Video players using AVKit (macOS 10.10+)
- Interactive maps using MapKit (macOS 10.9+)
- Web views using WebKit (macOS 10.10+)
"""

from ._base import *
from .basic import label


def video(
    url,
    dimensions=(320, 240),
    show_controls=True,
    autoplay=False,
    loop=False,
    border_radius=None,
):
    """Create a video player using AVKit.

    Args:
        url: Video URL (string path to local file or remote URL)
        dimensions: Tuple of (width, height) in points
        show_controls: Whether to show playback controls (default: True)
        autoplay: Whether to start playing automatically (default: False)
        loop: Whether to loop the video (default: False)
        border_radius: Optional corner radius in points (e.g., 8.0 for rounded corners)

    Returns:
        NSView containing AVPlayerView with video player

    Note:
        Requires macOS 10.10+. Returns empty view if AVKit is not available.
    """
    if not AVKIT_AVAILABLE:
        print("AVKit is not available. Video control requires macOS 10.10+")
        return NSView.alloc().init()

    width, height = dimensions

    # Create container view
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)
    container.setWantsLayer_(True)

    # Set size constraints
    container.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    container.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    try:
        # Convert URL string to NSURL
        if isinstance(url, str):
            if url.startswith("http://") or url.startswith("https://"):
                ns_url = NSURL.URLWithString_(url)
            else:
                # Local file path
                ns_url = NSURL.fileURLWithPath_(url)
        else:
            ns_url = url

        # Create AVPlayer with the video URL
        player = AVFoundation.AVPlayer.playerWithURL_(ns_url)

        # Create AVPlayerView
        player_view = AVKit.AVPlayerView.alloc().initWithFrame_(
            NSMakeRect(0, 0, width, height)
        )
        player_view.setPlayer_(player)
        player_view.setControlsStyle_(
            AVKit.AVPlayerViewControlsStyleDefault
            if show_controls
            else AVKit.AVPlayerViewControlsStyleNone
        )
        player_view.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Apply border radius if specified
        if border_radius is not None:
            player_view.setWantsLayer_(True)
            player_view.layer().setCornerRadius_(border_radius)
            player_view.layer().setMasksToBounds_(True)

        # Add to container
        container.addSubview_(player_view)

        # Pin player view to container edges
        player_view.topAnchor().constraintEqualToAnchor_(
            container.topAnchor()
        ).setActive_(True)
        player_view.bottomAnchor().constraintEqualToAnchor_(
            container.bottomAnchor()
        ).setActive_(True)
        player_view.leadingAnchor().constraintEqualToAnchor_(
            container.leadingAnchor()
        ).setActive_(True)
        player_view.trailingAnchor().constraintEqualToAnchor_(
            container.trailingAnchor()
        ).setActive_(True)

        # Handle looping if requested
        if loop:
            # Set up notification observer for when video ends
            from Foundation import NSNotificationCenter

            class VideoLoopHandler(NSObject):
                def initWithPlayer_(self, player):
                    self = objc.super(VideoLoopHandler, self).init()
                    if not self:
                        return None
                    self.player = player
                    return self

                def playerDidFinishPlaying_(self, notification):
                    """Restart video when it finishes"""
                    self.player.seekToTime_completionHandler_(
                        AVFoundation.CMTimeMake(0, 1),
                        lambda finished: self.player.play() if finished else None,
                    )

            # Create loop handler and register for notifications
            loop_handler = VideoLoopHandler.alloc().initWithPlayer_(player)
            NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
                loop_handler,
                "playerDidFinishPlaying:",
                AVFoundation.AVPlayerItemDidPlayToEndTimeNotification,
                player.currentItem(),
            )

            # Keep reference to prevent garbage collection
            _delegate_registry[id(player_view)] = loop_handler

        # Autoplay if requested
        if autoplay:
            player.play()

        return container

    except Exception as e:
        print(f"Error creating video player: {e}")
        # Return empty view on error
        error_label = label(f"Video load error", font_size=10, color="gray")
        container.addSubview_(error_label)
        error_label.centerXAnchor().constraintEqualToAnchor_(
            container.centerXAnchor()
        ).setActive_(True)
        error_label.centerYAnchor().constraintEqualToAnchor_(
            container.centerYAnchor()
        ).setActive_(True)
        return container


def map_view(
    latitude=37.7749,
    longitude=-122.4194,
    zoom=0.05,
    dimensions=(320, 240),
    map_type: Union[str, MapType] = MapType.STANDARD,
    show_controls=True,
    annotations=None,
    border_radius=None,
):
    """Create a map view using MapKit.

    Args:
        latitude: Center latitude coordinate (default: San Francisco)
        longitude: Center longitude coordinate (default: San Francisco)
        zoom: Zoom level as coordinate span in degrees (smaller = more zoomed in, default: 0.05)
        dimensions: Tuple of (width, height) in points
        map_type: Map type (MapType enum or legacy string)
                  Use MapType.STANDARD, .SATELLITE, .HYBRID, .SATELLITE_FLYOVER, .HYBRID_FLYOVER, .MUTED_STANDARD
        show_controls: Whether to show zoom and compass controls (default: True)
        annotations: List of annotation dicts with keys: 'latitude', 'longitude', 'title', 'subtitle' (optional)
        border_radius: Optional corner radius in points (e.g., 8.0 for rounded corners)

    Returns:
        NSView containing MKMapView

    Note:
        Requires macOS 10.9+. Returns empty view if MapKit is not available.
    """
    if not MAPKIT_AVAILABLE:
        print("MapKit is not available. Map control requires macOS 10.9+")
        return NSView.alloc().init()

    width, height = dimensions

    # Create container view
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)
    container.setWantsLayer_(True)

    # Set size constraints
    container.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    container.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    try:
        # Create MKMapView
        map_view = MapKit.MKMapView.alloc().initWithFrame_(
            NSMakeRect(0, 0, width, height)
        )
        map_view.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Set map type
        # Convert to enum if string, with deprecation warning
        map_type_enum = convert_map_type(map_type)
        mapkit_constant = map_type_enum.to_mapkit_constant()
        map_view.setMapType_(mapkit_constant if mapkit_constant is not None else MapKit.MKMapTypeStandard)

        # Set center coordinate and zoom level
        center = MapKit.CLLocationCoordinate2D()
        center.latitude = latitude
        center.longitude = longitude

        span = MapKit.MKCoordinateSpan()
        span.latitudeDelta = zoom
        span.longitudeDelta = zoom

        region = MapKit.MKCoordinateRegion()
        region.center = center
        region.span = span

        map_view.setRegion_animated_(region, False)

        # Configure controls
        map_view.setZoomEnabled_(show_controls)
        map_view.setScrollEnabled_(show_controls)
        map_view.setRotateEnabled_(show_controls)

        # Show compass and zoom controls if available (macOS 10.13+)
        if hasattr(map_view, "setShowsCompass_"):
            map_view.setShowsCompass_(show_controls)
        if hasattr(map_view, "setShowsZoomControls_"):
            map_view.setShowsZoomControls_(show_controls)

        # Add annotations if provided
        if annotations:
            for ann_data in annotations:
                if isinstance(ann_data, dict):
                    ann_lat = ann_data.get("latitude", latitude)
                    ann_lon = ann_data.get("longitude", longitude)
                    ann_title = ann_data.get("title", "")
                    ann_subtitle = ann_data.get("subtitle", "")

                    annotation = MapKit.MKPointAnnotation.alloc().init()
                    coord = MapKit.CLLocationCoordinate2D()
                    coord.latitude = ann_lat
                    coord.longitude = ann_lon
                    annotation.setCoordinate_(coord)

                    if ann_title:
                        annotation.setTitle_(str(ann_title))
                    if ann_subtitle:
                        annotation.setSubtitle_(str(ann_subtitle))

                    map_view.addAnnotation_(annotation)

        # Apply border radius if specified
        if border_radius is not None:
            map_view.setWantsLayer_(True)
            map_view.layer().setCornerRadius_(border_radius)
            map_view.layer().setMasksToBounds_(True)

        # Add to container
        container.addSubview_(map_view)

        # Pin map view to container edges
        map_view.topAnchor().constraintEqualToAnchor_(container.topAnchor()).setActive_(
            True
        )
        map_view.bottomAnchor().constraintEqualToAnchor_(
            container.bottomAnchor()
        ).setActive_(True)
        map_view.leadingAnchor().constraintEqualToAnchor_(
            container.leadingAnchor()
        ).setActive_(True)
        map_view.trailingAnchor().constraintEqualToAnchor_(
            container.trailingAnchor()
        ).setActive_(True)

        return container

    except Exception as e:
        print(f"Error creating map view: {e}")
        # Return empty view on error
        error_label = label(f"Map load error", font_size=10, color="gray")
        container.addSubview_(error_label)
        error_label.centerXAnchor().constraintEqualToAnchor_(
            container.centerXAnchor()
        ).setActive_(True)
        error_label.centerYAnchor().constraintEqualToAnchor_(
            container.centerYAnchor()
        ).setActive_(True)
        return container


def web_view(
    url=None,
    html=None,
    dimensions=(400, 300),
    enable_javascript=True,
    transparent=False,
    border_radius=None,
    private_mode=True,
    storage_path=None,
):
    """Create a web view using WebKit.

    Args:
        url: URL to load (string). Takes precedence over html parameter.
        html: HTML string to load (optional, used if url is None)
        dimensions: Tuple of (width, height) in points
        enable_javascript: Whether to enable JavaScript (default: True)
        transparent: Whether to use transparent background (default: False)
        border_radius: Optional corner radius in points (e.g., 8.0 for rounded corners)
        private_mode: If True, cookies and persistent storage are not saved between sessions (default: True)
        storage_path (Optional[str]): Optional identifier for persistent storage.
            Only used if `private_mode` is False. Creates a unique WebKit data store
            in ``/Library/WebKit/com.stackit.webkit.<hash>/``. Requires macOS 13.3+
            for custom identifiers; falls back to the default storage on older versions.

    Returns:
        NSView containing WKWebView

    Note:
        Requires macOS 10.10+. Returns empty view if WebKit is not available.
        Either url or html must be provided.
    """
    if not WEBKIT_AVAILABLE:
        print("WebKit is not available. Web view control requires macOS 10.10+")
        return NSView.alloc().init()

    width, height = dimensions

    # Create container view
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    container.setTranslatesAutoresizingMaskIntoConstraints_(False)
    container.setWantsLayer_(True)

    # Set size constraints
    container.widthAnchor().constraintEqualToConstant_(width).setActive_(True)
    container.heightAnchor().constraintEqualToConstant_(height).setActive_(True)

    try:
        # Create WKWebView configuration
        config = WebKit.WKWebViewConfiguration.alloc().init()

        # Configure data store based on private_mode
        if private_mode:
            # Use non-persistent (ephemeral) data store - nothing saved between sessions
            config.setWebsiteDataStore_(
                WebKit.WKWebsiteDataStore.nonPersistentDataStore()
            )
        else:
            # Use persistent data store
            if storage_path:
                # Custom storage path
                import os

                identifier = f"com.stackit.webkit.{abs(hash(storage_path))}"

                # Check if initWithIdentifier_ is available (macOS 13.3+)
                if hasattr(WebKit.WKWebsiteDataStore, "alloc") and hasattr(
                    WebKit.WKWebsiteDataStore.alloc(), "initWithIdentifier_"
                ):
                    try:
                        data_store = (
                            WebKit.WKWebsiteDataStore.alloc().initWithIdentifier_(
                                identifier
                            )
                        )
                        config.setWebsiteDataStore_(data_store)
                    except Exception as e:
                        print(
                            f"Warning: Could not create custom data store: {e}. Using default."
                        )
                        config.setWebsiteDataStore_(
                            WebKit.WKWebsiteDataStore.defaultDataStore()
                        )
                else:
                    # Fallback for older macOS versions
                    print(
                        "Note: Custom storage identifiers require macOS 13.3+. "
                        "Using default storage."
                    )
                    config.setWebsiteDataStore_(
                        WebKit.WKWebsiteDataStore.defaultDataStore()
                    )

            else:
                # Use default persistent data store
                config.setWebsiteDataStore_(
                    WebKit.WKWebsiteDataStore.defaultDataStore()
                )

        # Configure JavaScript
        preferences = WebKit.WKPreferences.alloc().init()
        preferences.setJavaScriptEnabled_(enable_javascript)
        config.setPreferences_(preferences)

        # Create WKWebView
        web_view = WebKit.WKWebView.alloc().initWithFrame_configuration_(
            NSMakeRect(0, 0, width, height), config
        )
        web_view.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Enable layer for both transparency and border radius
        web_view.setWantsLayer_(True)

        # Set transparent background if requested
        if transparent:
            # Make the web view itself transparent
            web_view.setOpaque_(False)
            web_view.setValue_forKey_(NSColor.clearColor(), "backgroundColor")

            # Set layer to transparent
            web_view.layer().setOpaque_(False)
            web_view.layer().setBackgroundColor_(NSColor.clearColor().CGColor())

            # Also make sure the underlying scroll view is transparent
            if hasattr(web_view, "scrollView"):
                web_view.scrollView().setDrawsBackground_(False)

        # Apply border radius if specified
        if border_radius is not None:
            web_view.layer().setCornerRadius_(border_radius)
            web_view.layer().setMasksToBounds_(True)

        # Load content
        if url:
            # Load from URL
            if isinstance(url, str):
                ns_url = NSURL.URLWithString_(url)
            else:
                ns_url = url
            request = Foundation.NSURLRequest.requestWithURL_(ns_url)
            web_view.loadRequest_(request)
        elif html:
            # Load HTML string
            web_view.loadHTMLString_baseURL_(html, None)
        else:
            # No content provided - load blank page
            web_view.loadHTMLString_baseURL_(
                "<html><body style='margin:0;padding:20px;font-family:system-ui;color:#888;'>No content loaded</body></html>",
                None,
            )

        # Add to container
        container.addSubview_(web_view)

        # Pin web view to container edges
        web_view.topAnchor().constraintEqualToAnchor_(container.topAnchor()).setActive_(
            True
        )
        web_view.bottomAnchor().constraintEqualToAnchor_(
            container.bottomAnchor()
        ).setActive_(True)
        web_view.leadingAnchor().constraintEqualToAnchor_(
            container.leadingAnchor()
        ).setActive_(True)
        web_view.trailingAnchor().constraintEqualToAnchor_(
            container.trailingAnchor()
        ).setActive_(True)

        return container

    except Exception as e:
        print(f"Error creating web view: {e}")
        import traceback

        traceback.print_exc()
        # Return empty view on error
        error_label = label(f"Web view load error", font_size=10, color="gray")
        container.addSubview_(error_label)
        error_label.centerXAnchor().constraintEqualToAnchor_(
            container.centerXAnchor()
        ).setActive_(True)
        error_label.centerYAnchor().constraintEqualToAnchor_(
            container.centerYAnchor()
        ).setActive_(True)
        return container


def window(
    title: str | None = None,
    size: tuple[int, int] = (600, 600),
    mask: int = AppKit.NSWindowStyleMaskTitled
    | AppKit.NSWindowStyleMaskClosable
    | AppKit.NSWindowStyleMaskMiniaturizable
    | AppKit.NSWindowStyleMaskResizable,
) -> AppKit.NSWindow:
    """Create a window with a title and size"""
    new_window = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(0, 0, *size),
        mask,
        AppKit.NSBackingStoreBuffered,
        False,
    )

    new_window.center()
    new_window.setTitlebarAppearsTransparent_(True)
    new_window.setTitleVisibility_(AppKit.NSWindowTitleHidden)
    new_window.setMovableByWindowBackground_(True)
    new_window.standardWindowButton_(AppKit.NSWindowCloseButton).setHidden_(False)
    new_window.standardWindowButton_(AppKit.NSWindowMiniaturizeButton).setHidden_(False)
    new_window.standardWindowButton_(AppKit.NSWindowZoomButton).setHidden_(False)

    new_window.makeKeyAndOrderFront_(None)
    if title is not None:
        new_window.setTitle_(title)

    return new_window


def window_layout(
    window: AppKit.NSWindow,
    layout: AppKit.NSView,
    padding: tuple[float, float, float, float] = (20.0, 20.0, 20.0, 20.0),
) -> AppKit.NSView:
    """Add a layout (stack or single control) to a window with proper constraints.

    This helper function simplifies adding StacKit layouts to windows by handling
    all the constraint setup automatically.

    Args:
        window: The NSWindow to add the layout to
        layout: A StackView (from hstack/vstack) or any NSView control
        padding: Edge insets as (top, leading, bottom, trailing) in points

    Returns:
        The layout view that was added (for reference)

    Example:
        >>> win = stackit.window(title="My App", size=(400, 300))
        >>> content = stackit.vstack([
        ...     stackit.label("Username:", bold=True),
        ...     stackit.text_field(placeholder="Enter username"),
        ...     stackit.button("Submit", callback=submit_handler)
        ... ], spacing=12.0)
        >>> stackit.window_layout(win, content, padding=(20, 20, 20, 20))
        >>> win.makeKeyAndOrderFront_(None)
    """
    # Ensure layout doesn't translate autoresizing mask
    layout.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Add layout to window's content view
    content_view = window.contentView()
    content_view.addSubview_(layout)

    # Unpack padding
    top, leading, bottom, trailing = padding

    # Pin layout to content view with padding
    layout.topAnchor().constraintEqualToAnchor_constant_(
        content_view.topAnchor(), top
    ).setActive_(True)
    layout.bottomAnchor().constraintEqualToAnchor_constant_(
        content_view.bottomAnchor(), -bottom
    ).setActive_(True)
    layout.leadingAnchor().constraintEqualToAnchor_constant_(
        content_view.leadingAnchor(), leading
    ).setActive_(True)
    layout.trailingAnchor().constraintEqualToAnchor_constant_(
        content_view.trailingAnchor(), -trailing
    ).setActive_(True)

    return layout
