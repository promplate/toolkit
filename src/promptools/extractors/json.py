from contextlib import suppress
from re import DOTALL, compile
from typing import Type, TypeVar, overload

from partial_json_parser import JSON, loads

F = TypeVar("F")
M = TypeVar("M")


@overload
def extract_json(text: str, /) -> JSON | None:
    ...


@overload
def extract_json(text: str, /, fallback: F) -> JSON | F:
    ...


@overload
def extract_json(text: str, /, fallback: F, expect: Type[M]) -> M | F:
    ...


def extract_json(text: str, /, fallback=None, expect=None):
    """parse JSON from raw LLM response text"""

    with suppress(IndexError):
        text = find_json_blocks(text)[-1]  # choose the last one

    with suppress(ValueError):
        result = loads(text)
        if expect is None:
            return result

        from pydantic import BaseModel, TypeAdapter, ValidationError

        with suppress(ValidationError):
            with suppress(TypeError):
                if issubclass(expect, BaseModel):
                    return expect.model_validate(result)
            return TypeAdapter(expect).validate_python(result)

    return fallback


json_block_pattern = compile(r"```json\n(.+?)(?:\n```|`{0,3}\Z)", DOTALL)


def find_json_blocks(text: str) -> list[str]:
    """find json code blocks from"""
    return json_block_pattern.findall(text)
