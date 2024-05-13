from contextlib import suppress
from functools import lru_cache, partial
from typing import TYPE_CHECKING

from pydantic import VERSION, BaseModel

if VERSION.startswith("1") and not TYPE_CHECKING:
    from pydantic import parse_raw_as

    @lru_cache(1)
    def get_json_validator(model_or_type_alias):
        return partial(parse_raw_as, model_or_type_alias)

else:
    from pydantic import TypeAdapter

    @lru_cache(1)
    def get_json_validator(model_or_type_alias):
        with suppress(TypeError):
            if issubclass(model_or_type_alias, BaseModel):
                return model_or_type_alias.model_validate_json

        return TypeAdapter(model_or_type_alias).validate_json
