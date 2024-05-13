from partial_json_parser import OBJ
from pydantic import BaseModel

from promptools.extractors import extract_json


def test_extract_partial_json():
    assert extract_json('{"a": 1, "b":') == {"a": 1}
    assert extract_json('{"a": 1', allow_partial=OBJ) == {}


def test_validate_partial_json():
    class Item(BaseModel):
        a: int
        b: str

    assert extract_json('{"a": 1, "b":', expect=Item) is None
    assert extract_json('{"a": 1, "b": "c', expect=Item) == Item(a=1, b="c")
