import tg_reader as tr
from tg_reader.datatypes import Events, Interval


def test_frames_on_synthetic_data() -> None:
    events = Events(
        events=[
            Interval(start=0, end=0.019, label="+"),
            Interval(start=0.041, end=0.059, label="-"),
        ]
    )
    frames = tr.events_to_frames(events, max_time=0.07)
    assert frames == ["+", "", "-"]
    frames = tr.events_to_frames(events, max_time=0.08)
    assert frames == ["+", "", "-", ""]


def test_events_to_events_with_nice_borders_and_nice_max_time() -> None:
    testevents = Events(
        events=[
            Interval(start=0, end=0.019, label="+"),
            Interval(start=0.041, end=0.06, label="-"),
        ]
    )

    frames = tr.events_to_frames(testevents, max_time=0.07)
    reconstructed_events = tr.frames_to_events(frames=frames).events
    expected_events = [
        Interval(start=0, end=0.02, label="+"),
        Interval(start=0.02, end=0.04, label=""),
        Interval(start=0.04, end=0.06, label="-"),
    ]
    assert reconstructed_events == expected_events


def test_events_to_events_with_nice_borders_and_longer_audio() -> None:
    testevents = Events(
        events=[
            Interval(start=0, end=0.019, label="+"),
            Interval(start=0.041, end=0.059, label="-"),
        ]
    )
    frames = tr.events_to_frames(testevents, max_time=0.07)
    returned_events = tr.frames_to_events(frames).events
    assert returned_events == [
        Interval(start=0, end=0.02, label="+"),
        Interval(start=0.02, end=0.04),
        Interval(start=0.04, end=0.06, label="-"),
    ]


def test_events_to_events_with_aligned_borders_and_nice_audio_length() -> None:
    testevents = Events(
        events=[
            Interval(start=0, end=0.02, label="+"),
            Interval(start=0.04, end=0.06, label="-"),
        ]
    )
    frames = tr.events_to_frames(testevents, max_time=0.08)
    returned_events = tr.frames_to_events(frames).events
    assert returned_events == [
        Interval(start=0, end=0.02, label="+"),
        Interval(start=0.02, end=0.04),
        Interval(start=0.04, end=0.06, label="-"),
        Interval(start=0.06, end=0.08),
    ]


def test_events_to_events_with_aligned_borders_and_lonter_audio() -> None:
    testevents = Events(
        events=[
            Interval(start=0, end=0.02, label="+"),
            Interval(start=0.04, end=0.06, label="-"),
        ]
    )
    frames = tr.events_to_frames(testevents, max_time=0.09)
    returned_events = tr.frames_to_events(frames).events
    assert returned_events == [
        Interval(start=0, end=0.02, label="+"),
        Interval(start=0.02, end=0.04),
        Interval(start=0.04, end=0.06, label="-"),
        Interval(start=0.06, end=0.08),
    ]
