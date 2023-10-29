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
[Item(index=0, label='A'), Item(index=1, label='B')]
```

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
