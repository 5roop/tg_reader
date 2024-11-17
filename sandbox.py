from pydantic import BaseModel, model_validator, field_validator
from typing import Self, Iterable, Any


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
    # @model_validator(mode="before")
    # @classmethod
    # def check_card_number_omitted(cls, data: Any) -> Any:
    #     for i in data["events"]:
    #         for j in data["events"]:
    #             if i == j:
    #                 continue
    #             if (i.start <= j.end) and (i.end >= j.start):
    #                 raise ValueError(
    #                     f"Found overlapping events: \n*{i} \n*{j}\n"
    #                 )
    #     data["events"] = sorted(data["events"], key=lambda i: i.start)
    #     return data

    @field_validator("events", mode="plain")
    def validate(cls, data):
        for i in data:
            for j in data:
                if i == j:
                    continue
                if (i.start <= j.end) and (i.end >= j.start):
                    raise ValueError(
                        f"Found overlapping events: \n*{i} \n*{j}\n"
                    )
        data = sorted(data, key=lambda i: i.start)
        return list(data)


a = Interval(start=1, end=2, label="")
b = Interval(start=2.1, end=2.5)


events = Events(events=[b, a])


2 + 2
