from contextlib import suppress
from re import DOTALL, compile

from partial_json_parser import ALL, ensure_json, loads


def extract_json(text: str, fallback=None, expect=None, allow_partial=ALL):
    """parse JSON from raw LLM response text"""

    with suppress(IndexError):
        text = find_json_blocks(text)[-1]  # choose the last one

    with suppress(ValueError):
        if expect is None:
            return loads(text, allow_partial)

        json = ensure_json(text, allow_partial)

        from pydantic import ValidationError

        from .validate import get_json_validator

        with suppress(ValidationError):
            return get_json_validator(expect)(json)

    return fallback


json_block_pattern = compile(r"```json\n(.+?)(?:\n```|`{0,3}\Z)", DOTALL)


def find_json_blocks(text):
    """find json code blocks from text"""
    return json_block_pattern.findall(text)
