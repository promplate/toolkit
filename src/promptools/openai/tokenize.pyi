from typing import Literal, NotRequired, TypedDict, overload

from tiktoken import Encoding

class Message(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str
    name: NotRequired[str]

@overload
def count_token(prompt: str, enc: Encoding | None = None) -> int: ...
@overload
def count_token(prompt: Message, enc: Encoding | None = None) -> int: ...
@overload
def count_token(prompt: list[Message], enc: Encoding | None = None) -> int: ...
