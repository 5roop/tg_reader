from pydantic import BaseModel, model_validator


class Interval(BaseModel):
    start: float
    end: float
    label: str

    @model_validator(mode="before")
    @classmethod
    def check_non_negative_duration(cls, data: dict[str, float | str]):
        assert data["start"] < data["end"]
        return data


a = Interval(start=1, end=2, label="")


2+2