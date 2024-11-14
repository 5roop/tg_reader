from pathlib import Path

import pytest

import tg_reader as tr

test_file = Path("sample_data/fgDDtwU4we4_15533.0-15538.76.TextGrid")


def test_event_generation() -> None:
    events = tr.tg_to_events(test_file)
    assert len(events) == 25
    assert events[0].label == "+"


def test_frame_generation() -> None:
    events = tr.tg_to_events(test_file)
    default_label = ""
    default_label = ""
    max_time = max([i.end for i in events])

    frames = tr.events_to_frames(
        events, default_label=default_label, max_time=max_time
    )
    assert set(frames) == set([i.label for i in events]).union(
        {default_label}
    ), "Sets of labels differ between frames and events..."
    assert len(frames) == int(50 * max_time)
    with pytest.raises(AssertionError):
        tr.events_to_frames(
            events,
            default_label=default_label,
            max_time=max_time,
            min_time=max_time + 1,
        )


def test_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        tr.frames_to_intervals(frames=[0, 0, 1])
