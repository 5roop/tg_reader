try:
    from typing import Any, Iterable, Self  # Available in Python 3.11 and later
except ImportError:
    from typing_extensions import Any, Iterable, Self

from pydantic import BaseModel, field_validator, model_validator


class Interval(BaseModel):
    start: float
    end: float
    label: str = ""

    @model_validator(mode="after")
    def check_duration(self: Self) -> Self:
        if self.start >= self.end:
            raise ValueError("Non-positive duration encountered!")
        return self


class Events(BaseModel):
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
