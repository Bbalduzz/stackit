#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DateTime StackIt Controls.

This module provides date and time controls like date pickers and time pickers
for user date/time input and selection.
"""

from ._base import *


def date_picker(
    style: int = AppKit.NSDatePickerStyleClockAndCalendar,
    elements: int = AppKit.NSDatePickerElementFlagYearMonthDay,
    mode: int = AppKit.NSDatePickerModeSingle,
    date: datetime.date | datetime.datetime | None = None,
    target: NSObject | None = None,
    action=None,
    size: tuple[int, int] = (200, 50),
    callback=None,
    **kwargs,
) -> NSDatePicker:
    """Create a date picker

    Args:
        style: style of the date picker, an AppKit.NSDatePickerStyle
        elements: elements to display in the date picker, an AppKit.NSDatePickerElementFlag
        mode: mode of the date picker, an AppKit.NSDatePickerMode
        date: initial date of the date picker; if None, defaults to the current date
        target: target to send action to (takes precedence over callback)
        action: action to send when the date is changed
        size: size of the date picker
        callback: Python function to call when date changes
        **kwargs: additional keyword/value attributes to configure

    Returns: NSDatePicker
    """
    date = date or datetime.date.today()
    date_picker = NSDatePicker.alloc().initWithFrame_(NSMakeRect(0, 0, *size))
    date_picker.setDatePickerStyle_(style)
    date_picker.setDatePickerElements_(elements)
    date_picker.setDatePickerMode_(mode)
    date_picker.setDateValue_(date)
    date_picker.setTimeZone_(NSTimeZone.localTimeZone())
    date_picker.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # Handle target/action vs callback
    if target and action:
        date_picker.setTarget_(target)
        date_picker.setAction_(action)
    elif callback:
        date_picker.setTarget_(NSApp)
        date_picker.setAction_("datePickerCallback:")
        # Register callback with delegate
        StackAppDelegate.register_callback(date_picker, None, callback)

    if kwargs:
        for key, value in kwargs.items():
            method = f"set{key[0].upper()}{key[1:]}_"
            if hasattr(date_picker, method):
                getattr(date_picker, method)(value)
    return date_picker


def time_picker(
    style: int = AppKit.NSDatePickerStyleTextFieldAndStepper,
    elements: int = AppKit.NSDatePickerElementFlagHourMinute,
    mode: int = AppKit.NSDatePickerModeSingle,
    time: datetime.datetime | datetime.time | None = None,
    target: NSObject | None = None,
    action=None,
    callback=None,
    **kwargs,
) -> NSDatePicker:
    """Create a time picker

    Args:
        style: style of the date picker, an AppKit.NSDatePickerStyle
        elements: elements to display in the date picker, an AppKit.NSDatePickerElementFlag
        mode: mode of the date picker, an AppKit.NSDatePickerMode
        time: initial time of the date picker; if None, defaults to the current time
        target: target to send action to (takes precedence over callback)
        action: action to send when the time is changed
        callback: Python function to call when time changes
        **kwargs: additional keyword/value attributes to configure

    Returns: NSDatePicker


    Note: This function is a wrapper around date_picker, with the date picker style set to
    display a time picker.
    """
    # if time is only a time, convert to datetime with today's date
    # as the date picker requires a datetime or date
    if isinstance(time, datetime.time):
        time = datetime.datetime.combine(datetime.date.today(), time)
    time = time or datetime.datetime.now()
    tp = date_picker(
        style=style,
        elements=elements,
        mode=mode,
        date=time,
        target=target,
        action=action,
        callback=callback,
    )
    if kwargs:
        for key, value in kwargs.items():
            method = f"set{key[0].upper()}{key[1:]}_"
            if hasattr(tp, method):
                getattr(tp, method)(value)
    return tp