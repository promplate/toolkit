from typing import NotRequired, TypedDict, overload

from tiktoken import Encoding

class Message(TypedDict):
    role: str
    content: str
    name: NotRequired[str]

@overload
def count_token(prompt: str, enc: Encoding | None = None) -> int: ...
@overload
def count_token(prompt: Message, enc: Encoding | None = None) -> int: ...
@overload
def count_token(prompt: list[Message], enc: Encoding | None = None) -> int: ...
