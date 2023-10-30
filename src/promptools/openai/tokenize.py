"""Count tokens for OpenAI models"""

from tiktoken import get_encoding


def count_token(prompt, enc=None):
    """count number of tokens in prompt"""

    enc = enc or get_encoding("cl100k_base")

    if isinstance(prompt, str):
        return len(enc.encode(prompt, disallowed_special=()))

    if isinstance(prompt, list):
        return 3 + sum(map(count_token, prompt))

    if isinstance(prompt, dict):
        return (
            3
            + (len(enc.encode(f"name={prompt['name']}")) if "name" in prompt else 1)
            + len(enc.encode(prompt["content"]))
        )

    raise TypeError(prompt)
