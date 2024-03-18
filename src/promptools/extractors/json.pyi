from re import Pattern
from typing import Type, TypeVar

from partial_json_parser import ALL, JSON, Allow

F = TypeVar("F")
M = TypeVar("M")

def extract_json(
    text: str,
    fallback: F = None,
    expect: Type[M] = type[JSON],
    allow_partial: Allow = ALL,
) -> M | F: ...

json_block_pattern: Pattern = ...

def find_json_blocks(text: str) -> list[str]: ...
