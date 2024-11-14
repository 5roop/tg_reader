import pytest
from praatio.utilities.constants import Interval

import tg_reader as tr


def test_frames_on_synthetic_data() -> None:
    events = [
        Interval(start=0, end=0.019, label="+"),
        Interval(start=0.041, end=0.059, label="-"),
    ]
    frames = tr.events_to_frames(events, default_label="", max_time=0.07)
    assert frames == ["+", "", "-"]
    frames = tr.events_to_frames(events, default_label="", max_time=0.08)
    assert frames == ["+", "", "-", ""]


test_frames_on_synthetic_data()


def test_events_to_events() -> None:
    events = [
        Interval(start=0, end=0.019, label="+"),
        Interval(start=0.041, end=0.06, label="-"),
    ]
    frames = tr.events_to_frames(events, default_label="", max_time=0.07)
    reconstructed_events = tr.frames_to_intervals(frames=frames)
    expected_events = [
        Interval(start=0, end=0.02, label="+"),
        Interval(start=0.02, end=0.04, label=""),
        Interval(start=0.04, end=0.06, label="-"),
    ]
    assert reconstructed_events == expected_events


def test_fails_on_overlapping_data() -> None:
    events = [
        Interval(start=0, end=0.2, label="+"),
        Interval(start=0.1, end=3, label="-"),
    ]
    with pytest.raises(Exception):
        tr.events_to_frames(events, default_label="", max_time=0.07)


def test_fails_on_nonpositive_interval_duration() -> None:
    events = [
        Interval(start=0, end=0.05, label="+"),
        Interval(start=0.1, end=0.06, label="-"),
    ]
    with pytest.raises(AssertionError):
        tr.events_to_frames(events, default_label="", max_time=0.07)
