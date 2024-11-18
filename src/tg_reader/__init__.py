__version__ = "2024.11.18"


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
    """Transforms textgrid Intervals into a list of labels.

    :param Events events: Intervals with attrib
    end, start, and label[str], wrapped in Events structure
    :param _type_ default_label: What to use in frames
    where no Interval is found, defaults to ""
    :return list[str]:
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
