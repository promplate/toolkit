# promptools

> useful utilities for prompt engineering

## Installation

```sh
pip install promptools  # or any other dependency manager you like
```

Note that the **validation** features use `pydantic>=2` as an optional dependencies. You can use `pip install promptools[validation]` to install it by the way.

## API References

### extractors

#### `extract_json`

parse JSON from raw LLM response text

##### Usages

Detect and parse the last JSON block from input string.

```py
def extract_json(text: str, /, fallback: F) -> JSON | F:
```

It will return `fallback` if it fails to detect / parse JSON.
Note that the default value of `fallback` is `None`.

```py
def extract_json(text: str, /, fallback: F, expect: Type[M]) -> M | F:
```

You can provide a `pydantic.BaseModel` or a `TypeAlias` in the `expect` parameter and `pydantic` will validate it.

##### Examples

###### Classification example

Imagine that you are using LLM on a classification task.

````py
from promptools.extractors import extract_json
from typing import TypedDict

class Item(TypedDict):
    index: int
    label: str

original_text = """
The result is:

```json
[
    {"index": 0, "label": "A"},
    {"index": 1, "label": "B"}
]
```
"""

print(extract_json(original_text, [], list[Item]))
````

The output will be:

```py
[{'index': 0, 'label': 'A'}, {'index': 1, 'label': 'B'}]
```

###### Streaming JSON example

Imagine that you are trying to parse a malformed JSON:

```py
from promptools.extractors import extract_json
from pydantic import BaseModel

original_text = '{"results": [{"index": 1}, {'

print(extract_json(original_text))
```

The output will be:

```py
{'results': [{'index': 1}, {}]}
```

### openai

#### `count_token`

count number of tokens in prompt

##### Usages

```py
def count_token(prompt: str | list[str], enc: Encoding | None = None) -> int:
```

Provide your prompt / a list of prompts, get its token count. The second parameter is the `tiktoken.Encoding` instance, will default to `get_encoding("cl100k_base")` if not provided. The default `tiktoken.Encoding` instance is cached, and will not be re-created every time.

```py
def count_token(prompt: dict | list[dict], enc: Encoding | None = None) -> int:
```

Note that it can also be a single message / a list of messages. Every message should be a dict in the schema below:

```py
class Message(TypedDict):
    role: str
    content: str
    name: NotRequired[str]
```

##### Examples

###### Plain text

```py
from tiktoken import encoding_for_model
from promptools.openai import count_token

print(count_token("hi", encoding_for_model("gpt-3.5-turbo")))
```

The output will be:

```py
1
```

##### List of plain texts

```py
from promptools.openai import count_token

print(count_token(["hi", "hello"]))
```

The output will be:

```py
2
```

###### Single message

```py
from promptools.openai import count_token

count_token({"role": "user", "content": "hi"})
```

The output will be:

```py
5
```

###### List of messages

```py
from promptools.openai import count_token

count_token([
    {"role": "user", "content": "hi"},
    {"role": "assistant", "content": "Hello! How can I assist you today?"},
])
```

The output will be:

```py
21
```

###### Integrating with `promplate`

```py
from promplate.prompt.chat import U, A, S
from promptools.openai import count_token

count_token([
    S @ "background" > "You are a helpful assistant.",
    U @ "example_user" > "hi",
    A @ "example_assistant" > "Hello! How can I assist you today?",
])
```

The output will be:

```py
40
```
