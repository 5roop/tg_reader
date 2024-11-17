import pytest
from pydantic import ValidationError

from tg_reader.datatypes import Events, Interval


def test_fails_on_overlapping_data() -> None:
    with pytest.raises(ValidationError):
        Events(
            events=[
                Interval(start=0, end=0.2, label="+"),
                Interval(start=0.1, end=3, label="-"),
            ]
        )


def test_fails_on_nonpositive_interval_duration() -> None:
    with pytest.raises(ValidationError):
        Events(
            events=[
                Interval(start=0, end=0.05, label="+"),
                Interval(start=0.1, end=0.06, label="-"),
            ]
        )
