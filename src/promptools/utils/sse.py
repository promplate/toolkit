from functools import wraps
from inspect import isasyncgen, isasyncgenfunction, isgenerator
from itertools import count
from typing import Any, Callable, Union

from attrs import asdict, define
from promplate import Template

_template = """\
{% if callable(id) -%}
id: {{ id() }}
{% elif id is not None -%}
id: {{ id }}
{% endif -%}
{% if event is not None -%}
event: {{ event }}
{% endif -%}
{% for line in data.splitlines() -%}
data: {{ line }}
{% endfor %}
"""

global_count = count()

event_template = Template(_template)


@define(slots=True, hash=True)
class Event:
    data: str
    event: Any = None
    id: Union[Callable[[], Any], Any] = global_count.__next__

    def __str__(self):
        return event_template.render(asdict(self))


def as_event_stream(gen, event=None):
    if isgenerator(gen):

        def _():
            for line in gen:
                yield str(Event(line, event))

        return _()

    if isasyncgen(gen):

        async def _():
            async for line in gen:
                yield str(Event(line, event))

        return _()

    assert callable(gen)

    if isasyncgenfunction(gen):

        @wraps(gen)
        async def _(*args, **kwargs):
            async for line in gen(*args, **kwargs):
                yield str(Event(line, event))

        return _

    @wraps(gen)
    def _(*args, **kwargs):
        return as_event_stream(gen(*args, **kwargs), event)

    return _
