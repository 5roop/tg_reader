from pathlib import Path

import pytest

import tg_reader as tr

test_file = Path("sample_data/fgDDtwU4we4_15533.0-15538.76.TextGrid")


def test_event_generation() -> None:
    events = tr.tg_to_events(test_file).events
    assert len(events) == 25
    assert events[0].label == "+"


def test_frame_generation() -> None:
    events = tr.tg_to_events(test_file)

    max_time = max([i.end for i in events.events])

    frames = tr.events_to_frames(events, max_time=max_time)
    assert set(frames) == set([i.label for i in events.events]).union(
        {""}
    ), "Sets of labels differ between frames and events..."
    assert len(frames) == int(50 * max_time)
    with pytest.raises(ValueError):
        tr.events_to_frames(
            events,
            max_time=max_time,
            min_time=max_time + 1,
        )
