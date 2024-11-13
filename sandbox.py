from pathlib import Path

import pandas as pd
from praatio import textgrid

# Open a textgrid with praatio:
sample_tg_path = Path("sample_data/fgDDtwU4we4_15533.0-15538.76.TextGrid")
tg = textgrid.openTextgrid(sample_tg_path, includeEmptyIntervals=False)

# Check tier names and pick the right one we need:
print(*[f"{i} : {n}" for i, n in enumerate(tg.tierNames)])
target_tier = 3

# Extract events and minimal and maximal time:
events = list(tg.tiers[target_tier])
min_time = min([i.start for i in events])
max_time = max([i.end for i in events])

# Get a range of 20ms Intervals with attributes left and right:
frames = pd.interval_range(start=min_time, end=max_time, freq=0.02)


labels = [None for i in frames]
# Iterate through the dataframe and assign labels from the tier elements
# When none exist, None will be used
for i, interval in enumerate(frames):
    for event in events:
        es, ee = event.start, event.end
        fs, fe = interval.left, interval.right
        if (es >= fe) and (fs <= ee):
            labels[i] = event.label

    break
# The resulting 20ms frame labels are the label column in the dataframe:
resulting_frames = labels
2 + 2
