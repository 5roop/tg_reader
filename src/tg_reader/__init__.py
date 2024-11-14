__version__ = "2024.11.13.2"


from pathlib import Path

import pandas as pd
from loguru import logger
from praatio.utilities.constants import Interval


def tg_to_events(inpath: str | Path, target_tier: int = 3) -> list[Interval]:
    from praatio import textgrid

    tg = textgrid.openTextgrid(inpath, includeEmptyIntervals=False)
    logger.debug(
        f"Tier {target_tier} = '{tg.tierNames[target_tier]}' is selected"
    )
    results = list(tg.tiers[target_tier])
    validate_events(results)
    return results


def events_to_frames(
    events: list[Interval],
    default_label: str = "",
    max_time: float = -6.66,
    min_time: float = 0.0,
) -> list[str]:
    """Transforms textgrid Intervals into a list of labels.

    :param list[Interval] events: Intervals with attrib
    end, start, and label[str]
    :param _type_ default_label: What to use in frames
    where no Interval is found, defaults to ""
    :return list[str]:
    """
    import pandas as pd

    validate_events(events)
    assert max_time > min_time
    frames = pd.interval_range(start=min_time, end=max_time, freq=0.02)
    labels = [default_label for i in frames]
    for i, frame in enumerate(frames):
        for event in events:
            es, ee = event.start, event.end
            fs, fe = frame.left, frame.right
            if (es <= fe) and (ee >= fs):
                labels[i] = event.label
    return labels


def frames_to_intervals(frames: list[str]) -> list[Interval]:
    # raise NotImplementedError(
    #     "This part has not yet been adapted to multi-target labels."
    #     "Go yell at the developer."
    # )

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
    return_list = [
        Interval(start=i[0] / 1e3, end=i[1] / 1e3, label=i[2])
        for i in event_list
    ]
    return return_list


def validate_events(events: list[Interval]) -> None:
    for i in events:
        assert i.start < i.end
    assert_non_overlapping(events)


def assert_non_overlapping(events: list[Interval]) -> None:
    for this in events:
        for other in events:
            if this == other:
                continue
            if (this.start < other.end) and (this.end > other.end):
                raise AssertionError("Events overlap!")
