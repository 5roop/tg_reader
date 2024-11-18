__version__ = "2024.11.18.1"


from pathlib import Path

import pandas as pd
from loguru import logger

try:
    from typing import Union
except ImportError:
    from typing_extensions import Union
from tg_reader.datatypes import Events, Interval


def tg_to_events(inpath: Union[str, Path], target_tier: int = 3) -> Events:
    from praatio import textgrid

    tg = textgrid.openTextgrid(inpath, includeEmptyIntervals=False)
    logger.debug(
        f"Tier {target_tier} = '{tg.tierNames[target_tier]}' is selected"
    )
    results = [
        Interval(start=i.start, end=i.end, label=i.label)
        for i in tg.tiers[target_tier]
    ]

    return Events(events=results)


def events_to_frames(
    events: Events,
    max_time: float = -6.66,
    min_time: float = 0.0,
) -> list[str]:
    """Transforms Events into a list of labels.
    Needs maxtime to know where to stop.

    If the last frame would end over max_time, it is skipped.
    E.g., for max_time = 0.03, only one frame is generated.

    Use as :

    .. code-block:: python
        events = Events(
            events=[
                Interval(start=0, end=0.02, label="+"),
                Interval(start=0.04, end=0.06, label="-"),
            ]
        )
        frames = frames_to_events(events, max_time=0.08)
        # Frames: ["+", "", "-", ""]
    :param Events events: _description_
    :param float max_time: until which time we need frames, defaults to -6.66,
    :param float min_time: min time, usually 0, defaults to 0.0
    :raises ValueError: Errors if max time is less or equal to min time.
    :return list[str]: Frames in 50Hz with string labels.
    """

    default_label = ""
    import pandas as pd

    if max_time <= min_time:
        raise ValueError("Min time is greater or equal to max time!")
    frames = pd.interval_range(start=min_time, end=max_time, freq=0.02)
    labels = [default_label for i in frames]
    for i, frame in enumerate(frames):
        for event in events.events:
            es, ee = event.start, event.end
            fs, fe = frame.left, frame.right
            if (es < fe) and (ee > fs):
                labels[i] = event.label
    return labels


def frames_to_events(frames: list[str]) -> Events:
    """Generate Events from frames. Pseudo-inverse of events_to_frames,
    except that it also generates Intervals with default label.
    Use as :

    .. code-block:: python
        events = Events(
            events=[
                Interval(start=0, end=0.02, label="+"),
                Interval(start=0.04, end=0.06, label="-"),
            ]
        )
        frames = frames_to_events(events, max_time=0.08)
        regenerated_events = events_to_frames(frames)
        regenerated_events
        # Returns Events(events=[
        #    Interval(start=0, end=0.02, label="+"),
        #    Interval(start=0.02, end=0.04),
        #    Interval(start=0.04, end=0.06, label="-"),
        #    Interval(start=0.06, end=0.08),
        #])
    :param list[str] frames: 50Hz frames with string labels
    :return Events: reconstructed events
    """
    ndf = pd.DataFrame(
        data={
            "millisecond_start": [20 * i for i in range(len(frames))],
            "frames": frames,
        }
    )
    ndf["millisecond_start"] = ndf.millisecond_start.astype(int)
    ndf["millisecond_end"] = ndf.millisecond_start + 20
    ndf["frames_next"] = ndf["frames"].shift(-1)

    # Filter rows where the frames value changes, including the last row
    events = ndf[ndf["frames"] != ndf["frames_next"]].copy()

    # Define start, end, and event value for each constant period
    events["start"] = events["millisecond_start"]
    events["end"] = events["millisecond_end"]
    events["event"] = events["frames"]

    # Select the relevant columns and convert to a list of lists
    event_list = events[["start", "end", "event"]].values.tolist()
    return_events = Events(
        events=[
            Interval(start=i[0] / 1e3, end=i[1] / 1e3, label=i[2])
            for i in event_list
        ]
    )
    return return_events
