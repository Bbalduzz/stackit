#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
StackIt UI Controls.

This module provides all the UI control factory functions for creating
native macOS interface elements that can be used in StackIt layouts.
"""

# Basic UI controls
from .basic import (
    label,
    link,
    image,
    button,
    spacer,
    separator,
)

# Input controls
from .input import (
    text_field,
    secure_text_input,
    search_field,
    slider,
    checkbox,
    combobox,
)

# Selection controls
from .selection import (
    radio_button,
    radio_group,
)

# Progress controls
from .progress import (
    progress_bar,
    circular_progress,
)

# Date/time controls
from .datetime import (
    date_picker,
    time_picker,
)

# Layout controls
from .layout import (
    block,
)

# Chart controls
from .charts import (
    line_chart,
    bar_chart,
    ring_chart,
)

# Media controls
from .media import (
    video,
    map_view,
    web_view,
)

# Window controls
from .window import (
    window,
    window_layout,
)

__all__ = [
    "label",
    "link",
    "image",
    "button",
    "spacer",
    "separator",
    "progress_bar",
    "circular_progress",
    "slider",
    "checkbox",
    "combobox",
    "text_field",
    "secure_text_input",
    "search_field",
    "radio_button",
    "radio_group",
    "date_picker",
    "time_picker",
    "block",
    "line_chart",
    "bar_chart",
    "ring_chart",
    "video",
    "map_view",
    "web_view",
    "window",
    "window_layout",
]