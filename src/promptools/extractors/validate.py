from contextlib import suppress
from functools import lru_cache, partial
from typing import TYPE_CHECKING

from pydantic import VERSION, BaseModel

if VERSION.startswith("1") and not TYPE_CHECKING:
    from pydantic import parse_obj_as

    @lru_cache(1)
    def get_validator(model_or_type_alias):
        return partial(parse_obj_as, model_or_type_alias)

else:
    from pydantic import TypeAdapter

    @lru_cache(1)
    def get_validator(model_or_type_alias):
        with suppress(TypeError):
            if issubclass(model_or_type_alias, BaseModel):
                return model_or_type_alias.model_validate

        return TypeAdapter(model_or_type_alias).validate_python
