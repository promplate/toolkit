from itertools import count
from typing import Any, AsyncIterator, Callable, Iterator, ParamSpec, TypeVar, overload

from attrs import asdict, define
from promplate import Template

_template: str

global_count: count

event_template: Template

@define(slots=True, hash=True)
class Event:
    data: str
    event: Any = None
    id: Callable[[], Any] | Any = global_count.__next__

AnyIterator = TypeVar("AnyIterator", Iterator[str], AsyncIterator[str])
P = ParamSpec("P")

@overload
def as_event_stream(gen: AnyIterator) -> AnyIterator: ...
@overload
def as_event_stream(gen: Callable[P, AnyIterator]) -> Callable[P, AnyIterator]: ...
