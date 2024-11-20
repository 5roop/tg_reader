from pydantic import BaseModel, field_validator, model_validator
from typing_extensions import Any, Iterable, Self


class Interval(BaseModel):
    """Model for intervals. Automatically generates default label ''
    if none is passed and validates duration (must be >0). Initiate as
    .. code-block:: python
      i = Interval(start=0, end=10, label="+")

    :param float start: start of the interval
    :param float end: end of the interval
    :param str label: label, arbitrary string, defaults to ''

    Examples:
    >>> Interval(start=0, end=10, label="+")
    Interval(start=0.0, end=10.0, label='+')

    >>> Interval(start=0, end=10)
    Interval(start=0.0, end=10.0, label='')


    """

    start: float
    end: float
    label: str = ""

    @model_validator(mode="after")
    def check_duration(self: Self) -> Self:
        if self.start >= self.end:
            raise ValueError("Non-positive duration encountered!")
        return self


class Events(BaseModel):
    """Model for validating a collection of intervals.

    Will not validate if events overlap. Events are sorted
    by start time.

    :param Iterable[Intervals] events: list or other iterable of Interval types.
    :raises ValidationError: when events overlap (but not when one ends exactly
    where the next ends.)

    .. code-block:: python
    >>> Events(events=[Interval(start=0, end=10, label="Hello")])
    Events(events=[Interval(start=0.0, end=10.0, label='Hello')])

    >>> Events(events=[
    ...  Interval(start=100, end=110, label="World"),
    ...  Interval(start=0, end=10, label="Hello"),
    ...  ])
    Events(events=[Interval(start=0.0, end=10.0, label='Hello'),...])
    """

    events: Iterable[Interval]

    @field_validator("events", mode="plain")
    def validate(cls: Any, data: Iterable[Interval]) -> Iterable[Interval]:
        for i in data:
            for j in data:
                if i == j:
                    continue
                if (i.start < j.end) and (i.end > j.start):
                    raise ValueError(
                        f"Found overlapping events: \n*{i} \n*{j}\n"
                    )
        data = sorted(data, key=lambda i: i.start)
        return list(data)
