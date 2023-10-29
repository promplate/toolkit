from re import Pattern
from typing import Type, TypeVar, overload

from partial_json_parser import JSON

F = TypeVar("F")
M = TypeVar("M")

@overload
def extract_json(text: str) -> JSON | None: ...
@overload
def extract_json(text: str, fallback: F) -> JSON | F: ...
@overload
def extract_json(text: str, fallback: F, expect: Type[M]) -> M | F: ...

json_block_pattern: Pattern = ...

def find_json_blocks(text: str) -> list[str]: ...
