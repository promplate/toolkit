from itertools import count
from typing import Any, AsyncIterator, Callable, Iterator, ParamSpec, TypeVar, overload

from attrs import define
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

type SyncAnyIterator = Iterator[str] | Iterator[tuple[str, Any]] | Iterator[tuple[str, Any, Callable[[], Any] | Any]]

type AsyncAnyIterator = AsyncIterator[str] | AsyncIterator[tuple[str, Any]] | AsyncIterator[tuple[str, Any, Callable[[], Any] | Any]]

@overload
def as_event_stream(gen: SyncAnyIterator) -> Iterator[Event]: ...
@overload
def as_event_stream(gen: AsyncAnyIterator) -> AsyncIterator[Event]: ...
@overload
def as_event_stream(gen: Callable[P, SyncAnyIterator]) -> Callable[P, Iterator[Event]]: ...
@overload
def as_event_stream(gen: Callable[P, AsyncAnyIterator]) -> Callable[P, AsyncIterator[Event]]: ...
