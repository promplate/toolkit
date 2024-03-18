from typing import Any, Callable, TypeVar

T = TypeVar("T")

def get_validator(model_or_type_alias: type[T]) -> Callable[[Any], T]: ...
