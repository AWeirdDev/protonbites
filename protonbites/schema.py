from dataclasses import Field, is_dataclass
from typing import Annotated, Any, ClassVar, Dict, Protocol, Type, get_origin

from .datatypes import DATATYPES


class DataclassType(Protocol):
    __dataclass_fields__: ClassVar[Dict[str, Any]]


class Schema:
    def __init__(self, __mapping: dict):
        self.mapping = __mapping

    def fit(self, array: list):
        ...


def get_schema(__dc: Type[DataclassType]):
    """🐣 Creates a schema from a dataclass.
    
    ```python
    @dataclass
    class Person:
        name: str
        age: int

    schema = get_schema(Person)
    ```
    """
    mapping = {}

    for name, field in __dc.__dataclass_fields__.items():
        if isinstance(field, Field):
            if get_origin(field.type) is Annotated:
                t = mapping[name] = field.type.__metadata__[0]
                assert t in DATATYPES
                mapping[name] = t

            elif is_dataclass(field.type):
                mapping[name] = get_schema(field.type)

            else:
                mapping[name] = field

        else:
            raise NotImplementedError(
                f"Not implemented for {type(field)!r} (field name {name!r})"
            )
        
    return Schema(mapping)
