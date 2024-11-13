__version__ = "2024.11.13.1"


from praatio.utilities.constants import Interval
from pathlib import Path
from loguru import logger
import pandas as pd


def tg_to_events(inpath: str | Path, target_tier: int = 3) -> list[Interval]:
    from praatio import textgrid

    tg = textgrid.openTextgrid(inpath, includeEmptyIntervals=False)
    logger.debug(f"Tier {target_tier} = '{tg.tierNames[target_tier]}' is selected")
    results = list(tg.tiers[target_tier])
    for this in results:
        for other in results:
            if this == other:
                continue
            if (this.start <= other.end) and (this.end >= other.end):
                raise ValueError("Events overlap!")
    return results


def events_to_frames(
    events: list[Interval],
    default_label=None,
    max_time: float = -6.66,
    min_time: float = 0.0,
) -> list[str]:
    """Transforms textgrid Intervals into a list of labels.

    :param list[Interval] events: Intervals with attrib end, start, and label[str]
    :param _type_ default_label: What to use in frames where no Interval is found, defaults to None
    :return list[str]:
    """
    import pandas as pd

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


def frames_to_intervals(frames: list[int]) -> list[pd.Interval]:
    raise NotImplementedError(
        "This part has not yet been adapted to multi-target labels. Go yell at the developer."
    )
    return_list = []
    ndf = pd.DataFrame(
        data={
            "millisecond": [20 * i for i in range(len(frames))],
            "frames": frames,
        }
    )

    ndf["millisecond"] = ndf.millisecond.astype(int)
    ndf = ndf.dropna()
    indices_of_change = ndf.frames.diff()[ndf.frames.diff() != 0].index.values
    for si, ei in pairwise(indices_of_change):
        if ndf.loc[si : ei - 1, "frames"].mode()[0] == 0:
            pass
        else:
            return_list.append(
                pd.Interval(ndf.loc[si, "millisecond"], ndf.loc[ei - 1, "millisecond"])
            )
    return return_list
