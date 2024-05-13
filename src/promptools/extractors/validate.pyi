from typing import Callable, TypeVar

T = TypeVar("T")

def get_json_validator(model_or_type_alias: type[T]) -> Callable[[str], T]: ...
