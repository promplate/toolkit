"""Count tokens for OpenAI models"""

from functools import lru_cache

from tiktoken import get_encoding

cached_get_encoding = lru_cache(1)(get_encoding)


def count_token(prompt, enc=None):
    """count number of tokens in prompt"""

    enc = enc or cached_get_encoding("cl100k_base")

    if isinstance(prompt, str):
        return len(enc.encode(prompt, disallowed_special=()))

    if isinstance(prompt, list):
        if len(prompt) == 0:
            return 0
        return sum(count_token(i, enc) for i in prompt) + (0 if isinstance(prompt[0], str) else 3)

    if isinstance(prompt, dict):
        return 3 + (len(enc.encode(f"name={prompt['name']}")) if "name" in prompt else 1) + len(enc.encode(prompt["content"]))

    raise TypeError(prompt)
