import typing

from pydantic import BaseModel as _BaseModel

T = typing.TypeVar("T", bound=type["BaseModel"])


class BaseModel(_BaseModel):
    class Config:
        anystr_strip_whitespace = True

    @classmethod
    def from_mapping(cls: T, mapping: typing.Mapping[str, typing.Any]) -> T:
        return cls(**{k: mapping[k] for k in cls.__fields__})

