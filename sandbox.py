from pydantic import BaseModel, model_validator
from typing import Self, Iterable


class Interval(BaseModel):
    start: float
    end: float
    label: str = ""

    @model_validator(mode="after")
    def check_duration(self) -> Self:
        if self.start >= self.end:
            raise ValueError("Non-positive duration encountered!")
        return self


class Events(BaseModel):
    events: Iterable[Interval]

    # def __init__(self, events: Iterable[Interval]) -> None:
    #     super(Events, self).__init__(events=events)

    @model_validator(mode="after")
    def check_overlapping(self) -> Self:
        from itertools import pairwise

        for i in self.events:
            for j in self.events:
                if i == j:
                    continue
                if (i.start <= j.end) and (i.end >= j.start):
                    raise ValueError(
                        f"Found overlapping events: \n*{i} \n*{j}\n"
                    )
        ordered = sorted(self.events, key=lambda i: i.start)
        self.events = ordered


a = Interval(start=1, end=2, label="")
b = Interval(start=2, end=2.5)


events = Events(events=[a, b])


2 + 2
