#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
StackIt - A minimal statusbar framework using only StackMenuItem

A completely isolated framework for creating macOS statusbar applications
using only StackMenuItem for rich layouts. No dependencies on the main
rumps library.
"""

__title__ = 'stackit'
__version__ = '0.2.0'
__author__ = 'Edoardo Balducci'
__license__ = 'MIT'

from .core import StackApp, MenuItem, StackView, hstack, vstack
from .utils import alert, notification, quit_application, timer, after, every, choose_directory, save_preferences, load_preferences
from .sfsymbol import SFSymbol
from .controls import (
    label, link, image, button, spacer, separator, progress_bar, circular_progress,
    slider, checkbox, combobox, text_field, secure_text_input, search_field, radio_button,
    date_picker, time_picker, block, line_chart
)

__all__ = [
    'StackApp',
    'MenuItem',
    'StackView',
    'hstack',
    'vstack',
    'SFSymbol',
    'alert',
    'notification',
    'quit_application',
    'timer',
    'after',
    'every',
    'choose_directory',
    'save_preferences',
    'load_preferences',
    'label',
    'link',
    'image',
    'button',
    'radio_button',
    'spacer',
    'separator',
    'progress_bar',
    'circular_progress',
    'slider',
    'checkbox',
    'combobox',
    'text_field',
    'secure_text_input',
    'search_field',
    'date_picker',
    'time_picker',
    'block',
    'line_chart'
]